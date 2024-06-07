import logging
from importlib.resources import files

from databricks.labs.lsql.backends import SqlBackend

import databricks.labs.remorph.resources

logger = logging.getLogger(__name__)


class TableDeployer:
    def __init__(self, sql_backend: SqlBackend, catalog: str, schema: str):
        self._sql_backend = sql_backend
        self._catalog = catalog
        self._schema = schema

    def deploy_table(self, table_name: str, relative_filepath: str):
        """
        Deploys a table to the catalog and schema specified in the constructor
        :param table_name: The table to deploy
        :param relative_filepath: DDL file path relative to the resource package
        """
        query = self._load(relative_filepath)
        logger.info(f"Deploying table {table_name} in {self._catalog}.{self._schema}")
        self._sql_backend.execute(query, catalog=self._catalog, schema=self._schema)

    def _load(self, relative_filename: str) -> str:
        sql = files(databricks.labs.remorph.resources).joinpath(relative_filename).read_text()
        return sql
