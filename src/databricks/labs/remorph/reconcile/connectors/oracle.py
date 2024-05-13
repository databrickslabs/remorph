from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, DataFrameReader, SparkSession
from sqlglot import Dialects

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.jdbc_reader import JDBCReaderMixin
from databricks.labs.remorph.reconcile.connectors.secrets import SecretsMixin
from databricks.labs.remorph.reconcile.constants import SourceDriver, SourceType
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema
from databricks.sdk import WorkspaceClient


class OracleDataSource(DataSource, SecretsMixin, JDBCReaderMixin):

    def __init__(
        self,
        engine: Dialects,
        spark: SparkSession,
        ws: WorkspaceClient,
        scope: str,
    ):
        self.engine = engine
        self.spark = spark
        self.ws = ws
        self.scope = scope

    @property
    def get_jdbc_url(self) -> str:
        return (
            f"jdbc:{SourceType.ORACLE.value}:thin:{self._get_secret_if_exists('user')}"
            f"/{self._get_secret_if_exists('password')}@//{self._get_secret_if_exists('host')}"
            f":{self._get_secret_if_exists('port')}/{self._get_secret_if_exists('database')}"
        )

    def read_query_data(
        self, catalog: str, schema: str, table: str, query: str, options: JdbcReaderOptions | None
    ) -> DataFrame:
        try:
            read_query = query.replace(":tbl", f"{schema}.{table}")
            if options is None:
                return self.reader(read_query).options(**self._get_timestamp_options()).load()
            options = self._get_jdbc_reader_options(options) | self._get_timestamp_options()
            return self.reader(read_query).options(**options).load()
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Oracle Data using the following {query} in OracleDataSource : {e!s}"
            )
            raise PySparkException(error_msg) from e

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        try:
            schema_query = self._get_schema_query(table, schema)
            schema_df = self.reader(schema_query).load()
            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Oracle Schema using the following {table} in "
                f"OracleDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    @staticmethod
    def _get_timestamp_options() -> dict[str, str]:
        return {
            "oracle.jdbc.mapDateToTimestamp": "False",
            "sessionInitStatement": """BEGIN dbms_session.set_nls('nls_date_format', '''YYYY-MM-DD''');
                                 dbms_session.set_nls('nls_timestamp_format', '''YYYY-MM-DD HH24:MI:SS''');
                           END;""",
        }

    def reader(self, query: str) -> DataFrameReader:
        return self._get_jdbc_reader(query, self.get_jdbc_url, SourceDriver.ORACLE.value)

    @staticmethod
    def _get_schema_query(table: str, owner: str) -> str:
        return f"""select column_name, case when (data_precision is not null
                                              and data_scale <> 0)
                                              then data_type || '(' || data_precision || ',' || data_scale || ')'
                                              when (data_precision is not null and data_scale = 0)
                                              then data_type || '(' || data_precision || ')'
                                              when data_precision is null and (lower(data_type) in ('date') or
                                              lower(data_type) like 'timestamp%') then  data_type
                                              when CHAR_LENGTH == 0 then data_type
                                              else data_type || '(' || CHAR_LENGTH || ')'
                                              end data_type
                                              FROM ALL_TAB_COLUMNS
                            WHERE lower(TABLE_NAME) = '{table}' and lower(owner) = '{owner}' """
