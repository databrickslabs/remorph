import logging
import os

from databricks.labs.lsql.backends import (
    DatabricksConnectBackend,
    RuntimeBackend,
    SqlBackend,
    StatementExecutionBackend,
)
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.base import DatabricksError

from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


def get_sql_backend(ws: WorkspaceClient, config: MorphConfig) -> SqlBackend:
    sdk_config = ws.config
    warehouse_id = isinstance(sdk_config.warehouse_id, str) and sdk_config.warehouse_id
    catalog_name = config.catalog_name
    schema_name = config.schema_name
    if warehouse_id:
        sql_backend = StatementExecutionBackend(ws, warehouse_id, catalog=catalog_name, schema=schema_name)
    else:
        sql_backend = RuntimeBackend() if "DATABRICKS_RUNTIME_VERSION" in os.environ else DatabricksConnectBackend(ws)
        try:
            sql_backend.execute(f"use catalog {catalog_name}")
            sql_backend.execute(f"use {schema_name}")
        except DatabricksError as dbe:
            logger.error(f"Catalog or Schema could not be selected: {dbe}")
            raise dbe
    logger.info(f"SQL Backend used for validation: {type(sql_backend).__name__}")
    return sql_backend
