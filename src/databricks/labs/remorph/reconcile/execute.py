import logging

from databricks.labs.remorph.helpers.execution_time import timeit

logger = logging.getLogger(__name__)


@timeit
def recon(recon_conf, conn_profile, source, report):
    logger.info(recon_conf)
    logger.info(conn_profile)
    logger.info(source)
    logger.info(report)
    pass
