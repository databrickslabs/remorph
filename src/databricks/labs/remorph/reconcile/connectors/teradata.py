import re
import logging
from datetime import datetime

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, DataFrameReader, SparkSession
from sqlglot import Dialect
from pyspark.sql.functions import col

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.jdbc_reader import JDBCReaderMixin
from databricks.labs.remorph.reconcile.connectors.secrets import SecretsMixin
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)

_SCHEMA_QUERY = """SELECT 
                     ColumnName as COLUMN_NAME,
                     CASE 
                        WHEN ColumnType IN ('I') 
                            THEN 'int'
                        WHEN ColumnType IN ('D')
                            THEN 'decimal(' || 
                                CAST(DecimalTotalDigits AS VARCHAR(100)) || ',' ||
                                CAST(DecimalFractionalDigits AS VARCHAR(100)) || ')'
                        WHEN ColumnType IN ('F') 
                                THEN 'float' 
                        WHEN ColumnLength IS NOT NULL AND ColumnType IN ('VC','CV') 
                                THEN 'varchar(' || CAST(ColumnLength AS VARCHAR(100)) || ')'
                        WHEN ColumnType = 'DT' 
                                THEN 'date'
                        WHEN ColumnType IN ('TS')
                                THEN 'timestamp'
                        WHEN ColumnType IN ('B')
                                THEN 'boolean'
                        WHEN ColumnType IN ('V')
                                THEN 'varchar'
                        ELSE 'string'
                    END DATA_TYPE
                    FROM 
                        DBC.ColumnsV
                    WHERE 
                    LOWER(TableName) = LOWER('{table}')
                    AND LOWER(DatabaseName) = LOWER('{schema}')
              """


class TeradataDataSource(DataSource, SecretsMixin, JDBCReaderMixin):
    _DRIVER = "teradata"

    def __init__(
        self,
        engine: Dialect,
        spark: SparkSession,
        ws: WorkspaceClient,
        secret_scope: str,
    ):
        self._engine = engine
        self._spark = spark
        self._ws = ws
        self._secret_scope = secret_scope

    @property
    def get_jdbc_url(self) -> str:
        # Fetch secrets once and store them in variables
        secrets = {key: self._get_secret(key) for key in ['CDE-BNSTLK-AZ-APPL-PWD']}
        #jdbc:teradata://edwd.corp.erac.com
        # Construct the JDBC URL
        return (
            f"jdbc:{self._DRIVER}://edwp.corp.erac.com/DBS_PORT=1025,"
            #f"databaseName={secrets['database']},"
            f"user=CDE_BNSTLK_AZ_APPL,"
            f"password={secrets['CDE-BNSTLK-AZ-APPL-PWD']},"
        )

    def read_data(
        self,
        catalog: str | None,
        schema: str,
        table: str,
        query: str,
        options: JdbcReaderOptions | None,
    ) -> DataFrame:
        table_query = query.replace(":tbl", f"{catalog}.{schema}.{table}")
        print(table_query)
        try:
            if options is None:
                df = self.reader(table_query).load()
            else:
                options = self._get_jdbc_reader_options(options)
                df = self._get_jdbc_reader(table_query, self.get_jdbc_url, self._DRIVER).options(**options).load()
            return df.select([col(column).alias(column.lower()) for column in df.columns])
        except (RuntimeError, PySparkException) as e:
            return self.log_and_throw_exception(e, "data", table_query)

    def get_schema(
        self,
        catalog: str | None,
        schema: str,
        table: str,
    ) -> list[Schema]:
        """
        Fetch the Schema from the DBC.ColumnsV table in Teradata.
        If the user's current role does not have the necessary privileges to access the specified
        Information Schema object, RunTimeError will be raised:
        "SQL access control error: Insufficient privileges to operate on schema 'DBC.ColumnsV' "
        """
        schema_query = re.sub(
            r'\s+',
            ' ',
            _SCHEMA_QUERY.format(catalog=catalog, schema=schema, table=table),
        )
        try:
            logger.debug(f"Fetching schema using query: \n`{schema_query}`")
            logger.info(f"Fetching Schema: Started at: {datetime.now()}")
            schema_metadata = self.reader(schema_query).load().collect()
            logger.info(f"Schema fetched successfully. Completed at: {datetime.now()}")
            return [Schema(field.COLUMN_NAME.lower(), field.DATA_TYPE.lower()) for field in schema_metadata]
        except (RuntimeError, PySparkException) as e:
            return self.log_and_throw_exception(e, "schema", schema_query)

    def reader(self, query: str) -> DataFrameReader:
        return self._get_jdbc_reader(query, self.get_jdbc_url, self._DRIVER)
