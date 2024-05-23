import logging
import pkgutil

from databricks.labs.lsql.backends import SqlBackend
from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)


class TableDeployer:
    def __init__(self, sql_backend: SqlBackend, morph_config: MorphConfig):
        self._sql_backend = sql_backend
        self._morph_config = morph_config

    def deploy_table(self, table_name: str, relative_filename: str):
        query = self._load(relative_filename)
        logger.info(
            f"Deploying table {table_name} in " f"{self._morph_config.catalog_name}.{self._morph_config.schema_name}"
        )
        self._sql_backend.execute(query)

    def _load(self, relative_filename: str) -> str:
        logger.info(f" Reading {relative_filename} contents")
        from databricks.labs import remorph

        data = pkgutil.get_data(remorph, relative_filename)
        assert data is not None
        sql = data.decode("utf-8")
        return sql
