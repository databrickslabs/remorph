from databricks.labs.blueprint.entrypoint import get_logger

from databricks.labs.remorph.helpers.execution_time import timeit

logger = get_logger(__file__)


@timeit
def recon(recon_conf, conn_profile, source, report):
    logger.info(recon_conf)
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)
    pass
