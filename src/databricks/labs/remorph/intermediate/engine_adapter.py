import logging
from pathlib import Path

from sqlglot.dialects.dialect import Dialect

from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine

logger = logging.getLogger(__name__)


class EngineAdapter:
    def __init__(self, dialect: str):
        self.dialect = dialect

    def select_engine(self, engine_type: str):
        if engine_type.lower() not in {"sqlglot"}:
            msg = f"Unsupported input type: {engine_type}"
            logger.error(msg)
            raise ValueError(msg)
        return SqlglotEngine()

    def parse_sql_content(self, dag, sql_content: str, file_path: str | Path, engine: str):
        # Not added type hints for dag as it is a cyclic import
        parser = self.select_engine(engine)
        for root_table, child in parser.parse_sql_content(self.dialect, sql_content, file_path):
            dag.add_node(child)
            dag.add_edge(root_table, child)
