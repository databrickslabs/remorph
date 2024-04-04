import logging
import os

from databricks.labs.lsql.backends import (
    DatabricksConnectBackend,
    RuntimeBackend,
    SqlBackend,
    StatementExecutionBackend,
)
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from databricks.sdk.errors.base import DatabricksError

from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


def initialise_catalog(sql_backend: SqlBackend, config: MorphConfig):
    catalog_name = config.catalog_name
    schema_name = config.schema_name
    try:
        sql_backend.execute(f"use catalog {catalog_name}")
        sql_backend.execute(f"use {schema_name}")
    except DatabricksError as dbe:
        logger.error(f"Catalog or Schema could not be selected: {dbe}")
        raise dbe


def get_sql_backend(ws: WorkspaceClient, config: MorphConfig) -> SqlBackend:
    sdk_config = Config(**config.sdk_config) if config.sdk_config else None
    warehouse_id = sdk_config.warehouse_id if sdk_config else None
    catalog_name = config.catalog_name
    schema_name = config.schema_name
    if warehouse_id:
        sql_backend = StatementExecutionBackend(ws, warehouse_id, catalog=catalog_name, schema=schema_name)
    else:
        # assigning cluster id explicitly to the config as user can provide it in the config
        ws.config.cluster_id = sdk_config.cluster_id
        sql_backend = RuntimeBackend() if "DATABRICKS_RUNTIME_VERSION" in os.environ else DatabricksConnectBackend(ws)
    logger.info(f"SQL Backend used for validation: {type(sql_backend).__name__}")
    return sql_backend
