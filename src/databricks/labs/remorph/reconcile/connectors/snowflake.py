import logging
import re

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, DataFrameReader, SparkSession
from pyspark.sql.functions import col
from sqlglot import Dialect

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.jdbc_reader import JDBCReaderMixin
from databricks.labs.remorph.reconcile.connectors.secrets import SecretsMixin
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


class SnowflakeDataSource(DataSource, SecretsMixin, JDBCReaderMixin):
    _DRIVER = "snowflake"
    _SCHEMA_QUERY = """select column_name, case when numeric_precision is not null and numeric_scale is not null then 
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then 
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        {catalog}.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='{table}' 
        and lower(table_schema) = '{schema}' order by ordinal_position"""

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
        return (
            f"jdbc:{SnowflakeDataSource._DRIVER}://{self._get_secret('sfAccount')}.snowflakecomputing.com"
            f"/?user={self._get_secret('sfUser')}&password={self._get_secret('sfPassword')}"
            f"&db={self._get_secret('sfDatabase')}&schema={self._get_secret('sfSchema')}"
            f"&warehouse={self._get_secret('sfWarehouse')}&role={self._get_secret('sfRole')}"
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
                    self._get_jdbc_reader(table_query, self.get_jdbc_url, SnowflakeDataSource._DRIVER)
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
        schema_query = re.sub(
            r'\s+',
            ' ',
            SnowflakeDataSource._SCHEMA_QUERY.format(catalog=catalog, schema=schema, table=table),
        )
        try:
            schema_df = self.reader(schema_query).load()
            return [Schema(field.COLUMN_NAME.lower(), field.DATA_TYPE.lower()) for field in schema_df.collect()]
        except (RuntimeError, PySparkException) as e:
            return self.log_and_throw_exception(e, "schema", schema_query)

    def reader(self, query: str) -> DataFrameReader:
        options = {
            "sfUrl": self._get_secret('sfUrl'),
            "sfUser": self._get_secret('sfUser'),
            "sfPassword": self._get_secret('sfPassword'),
            "sfDatabase": self._get_secret('sfDatabase'),
            "sfSchema": self._get_secret('sfSchema'),
            "sfWarehouse": self._get_secret('sfWarehouse'),
            "sfRole": self._get_secret('sfRole'),
        }
        return self._spark.read.format("snowflake").option("dbtable", f"({query}) as tmp").options(**options)
