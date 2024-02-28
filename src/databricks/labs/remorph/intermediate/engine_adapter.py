import logging
from pathlib import Path

from databricks.labs.remorph.intermediate.root_tables import DAG
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler

logger = logging.getLogger(__name__)


class EngineAdapter:
    def __init__(self, source: str):
        self.source = source

    def select_engine(self, input_type: str):
        if input_type.lower() == "sqlglot":
            return SQLTranspiler(self.source, [])
        else:
            msg = f"Unsupported input type: {input_type}"
            logger.error(msg)
            raise ValueError(msg)

    def parse_sql_content(self, dag: DAG, sql_content: str, file_name: str | Path, engine: str):
        parser = self.select_engine(engine)
        for root_table, child in parser.parse_sql_content(sql_content, file_name):
            dag.add_node(child)
            dag.add_edge(root_table, child)
