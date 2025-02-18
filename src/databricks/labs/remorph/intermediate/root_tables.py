import logging
from collections.abc import Iterable
from pathlib import Path
from sqlglot import parse, Expression, ErrorLevel
from sqlglot.expressions import Create, Insert, Merge, Join, Select, Table, With

from databricks.labs.remorph.helpers.file_utils import (
    get_sql_file,
    is_sql_file,
    read_file,
)
from databricks.labs.remorph.intermediate.dag import DAG

logger = logging.getLogger(__name__)


class RootTableAnalyzer:

    def __init__(self, source_dialect: str, input_path: Path):
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
        for root_table, child in self._analyse_table_lineage(sql_content, path):
            dag.add_node(child)
            dag.add_edge(root_table, child)

    def _analyse_table_lineage(self, source_code: str, file_path: Path) -> Iterable[tuple[str, str]]:
        parsed_expression, _ = parse(source_code, read=self.source_dialect, error_level=ErrorLevel.IMMEDIATE)
        if parsed_expression is not None:
            for expr in parsed_expression:
                child: str = str(file_path)
                if expr is not None:
                    # TODO: fix possible issue where the file reference is lost (if we have a 'create')
                    for change in expr.find_all(Create, Insert, Merge, bfs=False):
                        child = self._find_root_table(change)

                    for query in expr.find_all(Select, Join, With, bfs=False):
                        table = self._find_root_table(query)
                        if table:
                            yield table, child

    @staticmethod
    def _find_root_table(exp: Expression) -> str:
        table = exp.find(Table, bfs=False)
        return table.name if table else ""
