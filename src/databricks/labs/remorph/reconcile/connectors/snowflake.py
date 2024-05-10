import re

from databricks.sdk import WorkspaceClient
from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
from sqlglot import Dialects

from databricks.labs.remorph.reconcile.connectors.jdbc_reader import JDBCReaderMixin
from databricks.labs.remorph.reconcile.connectors.secrets import SecretsMixin
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver, SourceType
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class SnowflakeDataSource(DataSource, SecretsMixin, JDBCReaderMixin):

    def __init__(
            self,
            engine: Dialects,
            spark: SparkSession,
            ws: WorkspaceClient,
            scope: str,
    ):
        self._engine = engine
        self._spark = spark
        self._ws = ws
        self._scope = scope

    @property
    def get_jdbc_url(self) -> str:
        return (
            f"jdbc:{SourceType.SNOWFLAKE.value}://{self._get_secret_if_exists('sfAccount')}.snowflakecomputing.com"
            f"/?user={self._get_secret_if_exists('sfUser')}&password={self._get_secret_if_exists('sfPassword')}"
            f"&db={self._get_secret_if_exists('sfDatabase')}&schema={self._get_secret_if_exists('sfSchema')}"
            f"&warehouse={self._get_secret_if_exists('sfWarehouse')}&role={self._get_secret_if_exists('sfRole')}"
        )

    def read_query_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions | None) -> DataFrame:
        try:
            table_query = query.format(catalog_name=catalog, schema_name=schema)

            if options is None:
                df = self.reader(table_query)
            else:
                options = self._get_jdbc_reader_options(options)
                df = (
                    self._get_jdbc_reader(table_query, self.get_jdbc_url, SourceDriver.SNOWFLAKE.value)
                    .options(**options)
                    .load()
                )
            return df.select([col(column).alias(column.lower()) for column in df.columns])
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Data using the following {query} in "
                f"SnowflakeDataSource : {e!s}"
            )
            raise PySparkException(error_msg) from e

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        try:
            schema_query = self.get_schema_query(catalog, schema, table)
            schema_df = self.reader(schema_query).load()
            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Schema using the following {table} in "
                f"SnowflakeDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    def reader(self, query: str) -> DataFrame:
        options = {
            "sfUrl": self._get_secret_if_exists('sfUrl'),
            "sfUser": self._get_secret_if_exists('sfUser'),
            "sfPassword": self._get_secret_if_exists('sfPassword'),
            "sfDatabase": self._get_secret_if_exists('sfDatabase'),
            "sfSchema": self._get_secret_if_exists('sfSchema'),
            "sfWarehouse": self._get_secret_if_exists('sfWarehouse'),
            "sfRole": self._get_secret_if_exists('sfRole'),
        }
        return self._spark.read.format("snowflake").option("dbtable", f"({query}) as tmp").options(**options).load()

    @staticmethod
    def get_schema_query(catalog: str, schema: str, table: str):
        query = f"""select column_name, case when numeric_precision is not null and numeric_scale is not null then 
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then 
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        {catalog}.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='{table}' 
        and lower(table_schema) = '{schema}' order by ordinal_position"""
        return re.sub(r'\s+', ' ', query)

