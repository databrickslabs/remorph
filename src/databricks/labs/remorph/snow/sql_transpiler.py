import logging
from sqlglot import expressions as exp, parse, transpile
from sqlglot.dialects.dialect import Dialect
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.helpers.file_utils import refactor_hexadecimal_chars, format_error_message
from databricks.labs.remorph.helpers.morph_status import ParserError

logger = logging.getLogger(__name__)


class SqlglotEngine:
    def __init__(self, read_dialect: Dialect):
        self.read_dialect = read_dialect

    def transpile(
        self, write_dialect: Dialect, sql: str, file_name: str, error_list: list[ParserError]
    ) -> TranspilationResult:
        transpiled_sql_statements = []
        try:
            parsed_expressions = parse(sql, read=self.read_dialect, error_level=None)
            for expression in parsed_expressions:
                if expression is not None:
                    try:
                        sql = expression.sql(dialect=self.read_dialect)
                        transpiled_sql = transpile(
                            sql, read=self.read_dialect, write=write_dialect, pretty=True, error_level=ErrorLevel.RAISE
                        )
                        transpiled_sql_statements.extend(transpiled_sql)
                    except (ParseError, TokenError, UnsupportedError) as e:
                        logger.error(f"Error transpiling SQL from file {file_name} for expression: {expression}: {e}")
                        error_statement = format_error_message(e, str(expression))
                        transpiled_sql_statements.append(error_statement)
                        error_list.append(ParserError(file_name, refactor_hexadecimal_chars(str(e))))
        except (ParseError, TokenError, UnsupportedError) as e:
            transpiled_sql_statements = [""]
            error_statement = format_error_message(e, str(sql))
            transpiled_sql_statements.append(error_statement)
            logger.error(f"Error parsing SQL from file {file_name}: {e}")
            error_list.append(ParserError(file_name, refactor_hexadecimal_chars(str(e))))

        return TranspilationResult(transpiled_sql_statements, error_list)

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
