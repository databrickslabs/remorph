from sqlglot import expressions as exp, parse, transpile
from sqlglot.dialects.dialect import Dialect
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.helpers.file_utils import refactor_hexadecimal_chars
from databricks.labs.remorph.helpers.morph_status import ParserError


class SqlglotEngine:
    def __init__(self, read_dialect: Dialect):
        self.read_dialect = read_dialect

    def transpile(
        self, write_dialect: Dialect, sql: str, file_name: str, error_list: list[ParserError]
    ) -> TranspilationResult:
        try:
            transpiled_sql = transpile(sql, read=self.read_dialect, write=write_dialect, pretty=True, error_level=None)
        except (ParseError, TokenError, UnsupportedError) as e:
            transpiled_sql = [""]
            error_list.append(ParserError(file_name, refactor_hexadecimal_chars(str(e))))

        return TranspilationResult(transpiled_sql, error_list)

    def parse(self, sql: str, file_name: str) -> tuple[list[Expression | None] | None, ParserError | None]:
        expression = None
        error = None
        try:
            expression = parse(sql, read=self.read_dialect, error_level=ErrorLevel.IMMEDIATE)
        except (ParseError, TokenError, UnsupportedError) as e:
            error = ParserError(file_name, str(e))

        return expression, error

    def parse_sql_content(self, sql, file_name):
        parsed_expression, _ = self.parse(sql, file_name)
        if parsed_expression is not None:
            for expr in parsed_expression:
                child = str(file_name)
                if expr is not None:
                    for create in expr.find_all(exp.Create, exp.Insert, exp.Merge, bfs=False):
                        child = self._find_root_tables(create)

                    for select in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                        yield self._find_root_tables(select), child

    @staticmethod
    def _find_root_tables(expression) -> str | None:
        for table in expression.find_all(exp.Table, bfs=False):
            return table.name
        return None
