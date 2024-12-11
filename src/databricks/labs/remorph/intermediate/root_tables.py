import logging
from pathlib import Path

from databricks.labs.remorph.helpers.file_utils import (
    get_sql_file,
    is_sql_file,
    read_file,
)
from databricks.labs.remorph.intermediate.dag import DAG
from databricks.labs.remorph.intermediate.engine_adapter import EngineAdapter

logger = logging.getLogger(__name__)


class RootTableAnalyzer:
    def __init__(self, source_dialect: str, input_path: str | Path):
        self.source_dialect = source_dialect
        self.input_path = input_path
        self.engine_adapter = EngineAdapter(source_dialect)

    def generate_lineage_dag(self, engine="sqlglot") -> DAG:
        dag = DAG()

        # when input is sql file then parse the file
        if is_sql_file(self.input_path):
            filename = self.input_path
            logger.debug(f"Generating Lineage file: {filename}")
            sql_content = read_file(filename)
            self.engine_adapter.analyse_table_lineage(dag, sql_content, filename, engine)
            return dag  # return after processing the file

        # when the input is a directory
        for filename in get_sql_file(self.input_path):
            logger.debug(f"Generating Lineage file: {filename}")
            sql_content = read_file(filename)
            self.engine_adapter.analyse_table_lineage(dag, sql_content, filename, engine)

        return dag
