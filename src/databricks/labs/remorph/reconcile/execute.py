import json

from databricks.labs.blueprint.entrypoint import get_logger

from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.reconcile.recon_config import TableRecon

logger = get_logger(__file__)


@timeit
def recon(recon_conf, conn_profile, source, report):
    logger.info(recon_conf)
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)
    with open(recon_conf) as f:
        data = json.load(f)

    table_recon = TableRecon.from_dict(data)

    logger.info(table_recon)
    # TODO: Implement the rest of the function
    pass
