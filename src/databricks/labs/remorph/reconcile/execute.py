import logging
from pathlib import Path

from databricks.labs.blueprint.installation import Installation
from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import ReportType
from databricks.labs.remorph.reconcile.recon_config import Table
from databricks.labs.remorph.reconcile.reconciler import Reconciler

logger = logging.getLogger(__name__)


def recon(recon_conf, conn_profile, source, report):
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)

    table_recon = get_config(Path(recon_conf))

    raise NotImplementedError


class Reconciliation:
    def __init__(self, source: DataSource, target: DataSource, table_conf: Table, report_type: str):
        self.source = source
        self.target = target
        self.table_conf = table_conf
        self.report_type = report_type

    def run_reconcile(self):
        reconciler = Reconciler(
            source=self.source, target=self.target, table_conf=self.table_conf, report_type=self.report_type
        )
        if self.report_type == ReportType.ALL.value:
            reconciler.reconcile_data()
            reconciler.reconcile_schema()
        if self.report_type in {ReportType.DATA.value, ReportType.HASH.value}:
            reconciler.reconcile_data()
        if self.report_type == ReportType.SCHEMA.value:
            reconciler.reconcile_schema()
        else:
            raise ValueError("UNKNOWN REPORT TYPE")


def get_config(file: Path):
    # Convert the JSON data to the TableRecon dataclass
    return Installation.load_local(type_ref=TableRecon, file=file)
