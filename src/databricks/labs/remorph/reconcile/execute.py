import logging
from pathlib import Path

from databricks.labs.blueprint.installation import Installation
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import TableRecon, Tables

logger = logging.getLogger(__name__)


def recon(recon_conf, conn_profile, source, report):
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)

    table_recon = get_config(Path(recon_conf))

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
        source_data = self.source.read_data(schema_name, catalog_name, source_query, table_conf)
        target_data = self.target.read_data(schema_name, catalog_name, target_query, table_conf)
        print(source_data.printSchema())
        print(target_data.printSchema())

        # implement hash comparison
        # implement mismatch data
        # implement missing in source
        # implement missing in target
        # implement threshold comparison
        return False  # implement data comparison logic


def get_config(file: Path):
    # Convert the JSON data to the TableRecon dataclass
    return Installation.load_local(type_ref=TableRecon, file=file)
