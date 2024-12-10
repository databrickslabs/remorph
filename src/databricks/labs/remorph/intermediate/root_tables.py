import logging
from pathlib import Path

from databricks.labs.remorph.helpers.file_utils import (
    get_sql_file,
    is_sql_file,
    read_file,
)
from databricks.labs.remorph.intermediate.dag import DAG
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine

logger = logging.getLogger(__name__)


class RootTableLocator:
    def __init__(self, engine: TranspileEngine, source_dialect: str, input_path: Path):
        self.engine = engine
        self.source_dialect = source_dialect
        self.input_path = input_path

    def generate_lineage_dag(self) -> DAG:
        dag = DAG()

        # when input is sql file then parse the file
        if is_sql_file(self.input_path):
            logger.debug(f"Generating Lineage file: {self.input_path}")
            sql_content = read_file(self.input_path)
            self._populate_dag(sql_content, self.input_path, dag)
            return dag  # return after processing the file

        # when the input is a directory
        for path in get_sql_file(self.input_path):
            logger.debug(f"Generating Lineage file: {path}")
            sql_content = read_file(path)
            self._populate_dag(sql_content, path, dag)

        return dag

    def _populate_dag(self, sql_content: str, path: Path, dag: DAG):
        for root_table, child in self.engine.analyse_table_lineage(self.source_dialect, sql_content, path):
            dag.add_node(child)
            dag.add_edge(root_table, child)
