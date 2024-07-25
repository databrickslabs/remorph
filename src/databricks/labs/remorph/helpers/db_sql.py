import logging
import os

from databricks.labs.lsql.backends import (
    DatabricksConnectBackend,
    RuntimeBackend,
    SqlBackend,
    StatementExecutionBackend,
)
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def get_sql_backend(ws: WorkspaceClient, warehouse_id: str | None = None) -> SqlBackend:
    warehouse_id = warehouse_id or ws.config.warehouse_id
    if warehouse_id:
        sql_backend: SqlBackend = StatementExecutionBackend(ws, warehouse_id)
    else:
        sql_backend = RuntimeBackend() if "DATABRICKS_RUNTIME_VERSION" in os.environ else DatabricksConnectBackend(ws)
    return sql_backend
