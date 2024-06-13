import logging
import os

from databricks.labs.lsql.backends import (
    DatabricksConnectBackend,
    RuntimeBackend,
    SqlBackend,
    StatementExecutionBackend,
)
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


def get_sql_backend(ws: WorkspaceClient, config: MorphConfig) -> SqlBackend:
    sdk_config = config.sdk_config
    warehouse_id = sdk_config.get("warehouse_id", None) if sdk_config else None
    cluster_id = sdk_config.get("cluster_id", None) if sdk_config else None
    catalog_name = config.catalog_name
    schema_name = config.schema_name
    if warehouse_id:
        sql_backend: SqlBackend = StatementExecutionBackend(ws, warehouse_id, catalog=catalog_name, schema=schema_name)
    else:
        # Assigning cluster id explicitly to the config as user can provide them during installation
        ws.config.cluster_id = cluster_id if cluster_id else ws.config.cluster_id
        sql_backend = RuntimeBackend() if "DATABRICKS_RUNTIME_VERSION" in os.environ else DatabricksConnectBackend(ws)
    logger.info(f"SQL Backend used for validation: {type(sql_backend).__name__}")
    return sql_backend
