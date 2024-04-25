import logging
from pathlib import Path

from databricks.labs.blueprint.installation import Installation
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import Table, TableRecon

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

    def compare_schemas(self, table_conf: Table, schema_name: str, catalog_name: str) -> bool:
        raise NotImplementedError

    def compare_data(self, table_conf: Table, schema_name: str, catalog_name: str) -> bool:
        raise NotImplementedError


def get_config(file: Path):
    # Convert the JSON data to the TableRecon dataclass
    return Installation.load_local(type_ref=TableRecon, file=file)
