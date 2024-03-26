import logging
from pathlib import Path

from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.helpers.file_utils import (
    get_sql_file,
    is_sql_file,
    read_file,
)
from databricks.labs.remorph.intermediate.engine_adapter import EngineAdapter

logger = logging.getLogger(__name__)


class InferSchema:
    def __init__(self, ws: WorkspaceClient, source: str, input_path: str | Path):
        self._ws = ws
        self.source = source
        self.input_path = input_path

    @property
    def get_engine(self):
        return EngineAdapter(self.source)

    @classmethod
    def for_cli(cls, ws: WorkspaceClient, source: str, input_path: str | Path):
        return cls(ws, source, input_path)

    def apply(self, engine: str = "sqlglot") -> dict:
        table_column_mapping = {}

        if is_sql_file(self.input_path):
            filename = self.input_path
            logger.debug(f"Generating Schema from file: {filename}")
            sql_content = read_file(filename)
            table_column_mapping = self.get_engine.table_column_mapping(sql_content, filename, engine)
            return self._generate_create_table_statements(table_column_mapping)  # return after processing the file

        # when the input is a directory
        for filename in get_sql_file(self.input_path):
            logger.debug(f"Generating Schema from file: {filename}")
            sql_content = read_file(filename)
            table_column_mapping.update(self.get_engine.table_column_mapping(sql_content, filename, engine))

        return self._generate_create_table_statements(table_column_mapping)

    @staticmethod
    def _generate_create_table_statements(table_column_mapping: dict) -> dict:
        create_table_statements = {}

        for table, columns in table_column_mapping.items():
            columns_with_types = [f"{column} string" for column in columns]
            columns_string = ", ".join(columns_with_types)
            create_table_statement = f"CREATE TABLE {table} ({columns_string});"
            create_table_statements[table] = create_table_statement

        return create_table_statements
