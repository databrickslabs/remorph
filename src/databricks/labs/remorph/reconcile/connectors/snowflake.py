import snowflake.connector
from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class SnowflakeDataSource(DataSource):

    @property
    def get_jdbc_url(self) -> str:
        if 'sfRole' not in self.connection_params:
            url = f"jdbc:{self.source}://{self.connection_params['account']}.snowflakecomputing.com/?user={self.connection_params['sfUser']}&password={self.connection_params['sfPassword']}&db={self.connection_params['sfDatabase']}&schema={self.connection_params['sfSchema']}&warehouse={self.connection_params['sfWarehouse']}"
        else:
            url = f"jdbc:{self.source}://{self.connection_params['account']}.snowflakecomputing.com/?user={self.connection_params['sfUser']}&password={self.connection_params['sfPassword']}&db={self.connection_params['sfDatabase']}&schema={self.connection_params['sfSchema']}&warehouse={self.connection_params['sfWarehouse']}&role={self.connection_params['sfRole']}"
        return url

    def read_data(self, schema_name: str, catalog_name: str, table_or_query: str, table_conf: Tables) -> DataFrame:
        if table_conf.jdbc_reader_options is None:
            df = (
                self.spark.read.format("snowflake")
                .option("dbtable", f"({table_or_query}) as tmp")
                .options(**self.connection_params)
                .load()
            )
        else:
            df = (
                self._get_jdbc_reader(table_or_query, self.get_jdbc_url, SourceDriver.SNOWFLAKE.value)
                .options(**self._get_jdbc_reader_options(table_conf.jdbc_reader_options))
                .load()
            )
        return df

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> list[Schema]:
        full_table_name = f"{catalog_name}.{schema_name}.{table_name}"

        sf_params = {
            "account": self.connection_params['account'],
            "user": self.connection_params['sfUser'],
            "password": self.connection_params['sfPassword'],
            "database": self.connection_params['sfDatabase'],
            "schema": self.connection_params['sfSchema'],
            "warehouse": self.connection_params['sfWarehouse'],
            "role": self.connection_params.get('sfRole', None),
        }

        con = snowflake.connector.connect(**sf_params)
        cursor = con.cursor()

        data = cursor.execute(f"describe table {full_table_name}").fetchall()
        # Extract only the "col_name" and "data_type" columns
        schema = [Schema(row[0].lower(), row[1].lower()) for row in data]
        return schema

    snowflake_datatype_mapper = {}
