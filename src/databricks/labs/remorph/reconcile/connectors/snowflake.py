import logging
import re

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, DataFrameReader, SparkSession
from pyspark.sql.functions import col
from sqlglot import Dialect

from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.jdbc_reader import JDBCReaderMixin
from databricks.labs.remorph.reconcile.connectors.secrets import SecretsMixin
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema, Table
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
                logger.debug(f"JDBC URL: {self.get_jdbc_url}")
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
            logger.info(f"Fetching Snowflake Schema using the following {table} in SnowflakeDataSource")
            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
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
        logger.debug(f"Reading data from Snowflake using the options {options.keys()} ")
        return self._spark.read.format("snowflake").option("dbtable", f"({query}) as tmp").options(**options)

    def list_tables(
        self,
        catalog: str | None,
        schema: str,
        include_list: list[str] | None,
        exclude_list: list[str] | None,
    ) -> TableRecon:

        filter_list = None
        in_clause = None

        if include_list:
            filter_list = include_list
            in_clause = "IN"

        if exclude_list:
            filter_list = exclude_list
            in_clause = "NOT IN"

        where_cond = ""
        if filter_list:
            subset_tables = ", ".join(filter_list)
            where_cond = f"AND TABLE_NAME {in_clause} ({subset_tables})"

        assert catalog, "Catalog must be specified for Snowflake DataSource"
        try:
            logger.debug(f"Fetching Snowflake Table list for `{catalog}.{schema}`")
            tables_query = f"""SELECT TABLE_NAME, CLUSTERING_KEY, ROW_COUNT\n 
                               FROM {catalog.upper()}.INFORMATION_SCHEMA.TABLES\n 
                               WHERE TABLE_SCHEMA = '{schema.upper()}' {where_cond}"""

            logger.info(f" Executing query: {tables_query}")
            tables_df = self.reader(tables_query).load()

            tables_list = [
                Table(source_name=field.TABLE_NAME.lower(), target_name=field.TABLE_NAME.lower())
                for field in tables_df.collect()
            ]

            table_recon = TableRecon(
                source_catalog=catalog,
                source_schema=schema,
                target_catalog="",
                target_schema="",
                tables=tables_list,
            )

            return table_recon
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Table list for `{catalog}.{schema}`  in "
                f"SnowflakeDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e
