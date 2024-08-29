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


class SqlServerDataSource(DataSource, SecretsMixin, JDBCReaderMixin):
    _DRIVER = "sqlserver"
    _SCHEMA_QUERY = """SELECT 
                         COLUMN_NAME,
                         CASE
                            WHEN NUMERIC_PRECISION IS NOT NULL AND NUMERIC_PRECISION < 10 AND NUMERIC_PRECISION_RADIX = 10 AND NUMERIC_SCALE = 0 
                                THEN 'smallint' 
                            WHEN NUMERIC_PRECISION IS NOT NULL AND NUMERIC_PRECISION_RADIX = 10 AND NUMERIC_SCALE = 0 
                                THEN DATA_TYPE  
                            WHEN NUMERIC_PRECISION IS NOT NULL AND NUMERIC_PRECISION_RADIX = 10 AND NUMERIC_SCALE IS NOT NULL 
                                THEN 'decimal' + '(' + CAST(NUMERIC_PRECISION AS VARCHAR) + ',' + CAST(NUMERIC_SCALE AS VARCHAR) + ')'
                            WHEN NUMERIC_PRECISION IS NOT NULL AND NUMERIC_PRECISION_RADIX = 2 AND NUMERIC_SCALE IS NULL
                                THEN 'float' 
                            WHEN CHARACTER_MAXIMUM_LENGTH is NOT NULL AND CHARACTER_SET_NAME IS NOT NULL
                                THEN 'string' 
                            WHEN DATA_TYPE = 'date' 
                                THEN DATA_TYPE
                            WHEN DATA_TYPE IN ('time','datetime', 'datetime2', 'smalldatetime','datetimeoffset')
                                THEN 'timestamp'
                            WHEN DATA_TYPE IN ('bit')
                                THEN 'boolean'
                            WHEN CHARACTER_MAXIMUM_LENGTH is NOT NULL AND DATA_TYPE IN ('binary','varbinary','image')
                                THEN 'binary'
                            ELSE DATA_TYPE
                        END AS 'DATA_TYPE'
                        FROM 
                            INFORMATION_SCHEMA.COLUMNS
                        WHERE 
                        LOWER(TABLE_NAME) = LOWER('{table}')
                        AND LOWER(TABLE_SCHEMA) = LOWER('{schema}')
                        AND LOWER(TABLE_CATALOG) = LOWER('{catalog}')
                  """

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
        secrets = {key: self._get_secret(key) for key in
                   ['host', 'port', 'database', 'user', 'password','encrypt','trustServerCertificate']}

        # Construct the JDBC URL
        return (
            f"jdbc:{SqlServerDataSource._DRIVER}://{secrets['host']}:{secrets['port']};"
            f"databaseName={secrets['database']};"
            f"user={secrets['user']};"
            f"password={secrets['password']};"
            f"encrypt={secrets['encrypt']};"
            f"trustServerCertificate={secrets['trustServerCertificate']};"
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
        try:
            if options is None:
                df = self.reader(table_query).load()
            else:
                options = self._get_jdbc_reader_options(options)
                df = (
                    self._get_jdbc_reader(table_query, self.get_jdbc_url, SqlServerDataSource._DRIVER)
                    .options(**options)
                    .load()
                )
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
        Fetch the Schema from the INFORMATION_SCHEMA.COLUMNS table in SQL Server.

        If the user's current role does not have the necessary privileges to access the specified
        Information Schema object, RunTimeError will be raised:
        "SQL access control error: Insufficient privileges to operate on schema 'INFORMATION_SCHEMA' "
        """
        schema_query = re.sub(
            r'\s+',
            ' ',
            SqlServerDataSource._SCHEMA_QUERY.format(catalog=catalog, schema=schema, table=table),
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
        return self._get_jdbc_reader(query, self.get_jdbc_url, SqlServerDataSource._DRIVER)
