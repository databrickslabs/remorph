from pyspark.errors import PySparkException
from pyspark.sql import DataFrame, DataFrameReader

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class OracleDataSource(DataSource):

    # TODO need to check schema_name,catalog_name is needed
    # TODO rename the table_or_query
    def read_data(self, schema_name: str, catalog_name: str, table_or_query: str, table_conf: Tables) -> DataFrame:
        try:
            if table_conf.jdbc_reader_options is None:
                return self.reader(table_or_query).options(**self._get_timestamp_options()).load()
            else:
                return (
                    self.reader(table_or_query)
                    .options(
                        **self._get_jdbc_reader_options(table_conf.jdbc_reader_options) | self._get_timestamp_options()
                    )
                    .load()
                )
        except PySparkException as e:
            error_msg = f"An error occurred while fetching Oracle Data using the following {table_or_query} in OracleDataSource : {e!s}"
            raise PySparkException(error_msg) from e

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> list[Schema]:
        try:
            schema_query = self._get_schema_query(table_name, schema_name)
            schema_df = self.reader(schema_query).load()
            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = f"An error occurred while fetching Oracle Schema using the following {table_name} in OracleDataSource: {e!s}"
            raise PySparkException(error_msg) from e

    oracle_datatype_mapper = {
        "date": "coalesce(trim(to_char({},'YYYY-MM-DD')),'')",
    }

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
    def _get_schema_query(table_name: str, owner: str) -> str:
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
                            WHERE lower(TABLE_NAME) = '{table_name}' and lower(owner) = '{owner}' """
