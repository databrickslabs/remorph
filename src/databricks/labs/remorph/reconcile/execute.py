import json
import logging

from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import TableRecon, Tables

logger = logging.getLogger(__name__)


@timeit
def recon(recon_conf, conn_profile, source, report):
    logger.info(recon_conf)
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)

    with open(recon_conf, 'r') as f:
        data = json.load(f)

    # Convert the JSON data to the TableRecon dataclass
    table_recon = TableRecon.from_dict(data)

    for tables_conf in table_recon.tables:
        reconcile = Reconciliation(source, report)
        reconcile.compare_schemas(tables_conf, "schema", "catalog")
        reconcile.compare_data(tables_conf, "schema", "catalog")


class Reconciliation:
    def __init__(self, source: DataSource, target: DataSource):
        self.source = source
        self.target = target

    def compare_schemas(self, table_conf: Tables, schema_name: str, catalog_name: str) -> bool:
        source_schema = self.source.get_schema(table_conf.source_name, schema_name, catalog_name)
        target_schema = self.target.get_schema(table_conf.target_name, schema_name, catalog_name)
        return source_schema == target_schema

    def compare_data(self, table_conf: Tables, schema_name: str, catalog_name: str) -> bool:
        source_query = ""  # implement query builder
        target_query = ""  # implement query builder
        source_data = self.source.read_data(table_conf.source_name, schema_name, catalog_name, source_query)
        target_data = self.target.read_data(table_conf.target_name, schema_name, catalog_name, target_query)
        print(source_data.printSchema())
        print(target_data.printSchema())

        # implement hash comparison
        # implement mismatch data
        # implement missing in source
        # implement missing in target
        # implement threshold comparison
        return False  # implement data comparison logic
