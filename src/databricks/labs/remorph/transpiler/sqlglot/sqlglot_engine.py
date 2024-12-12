import logging
import typing as t
from sqlglot import expressions as exp, parse, transpile
from sqlglot.dialects.dialect import Dialect
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression
from sqlglot.tokens import Token, TokenType

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.helpers.string_utils import format_error_message, refactor_hexadecimal_chars
from databricks.labs.remorph.transpiler.transpile_status import ParserError

logger = logging.getLogger(__name__)


class ParsedExpression:
    def __init__(self, expression: exp.Expression, original_sql: str):
        self.parsed_expression = expression
        self.original_sql = original_sql


class SqlglotEngine:
    def __init__(self, read_dialect: Dialect):
        self.read_dialect = read_dialect

    def __partial_transpile(
        self, write_dialect: Dialect, sql: str, file_name: str, error_list: list[ParserError]
    ) -> tuple[list[str], list[ParserError]]:
        transpiled_sql_statements = []
        parsed_expressions, errors = self.safe_parse(statements=sql, read=self.read_dialect)
        for parsed_expression in parsed_expressions:
            if parsed_expression.parsed_expression is not None:
                try:
                    transpiled_sql = write_dialect.generate(parsed_expression.parsed_expression, pretty=True)

                    # Checking if the transpiled SQL is a comment and raise an error
                    if transpiled_sql.startswith("--"):
                        raise UnsupportedError("Unsupported SQL")
                    transpiled_sql_statements.append(transpiled_sql)
                except ParseError as e:
                    error_statement = format_error_message("Parsing Error", e, parsed_expression.original_sql)
                    errors.append(error_statement)
                except UnsupportedError as e:
                    error_statement = format_error_message("Unsupported SQL Error", e, parsed_expression.original_sql)
                    errors.append(error_statement)
                except TokenError as e:
                    error_statement = format_error_message("Token Error", e, parsed_expression.original_sql)
                    errors.append(error_statement)
        updated_error_list = self._handle_errors(errors, error_list, file_name, transpiled_sql_statements)
        return transpiled_sql_statements, updated_error_list

    def transpile(
        self, write_dialect: Dialect, sql: str, file_name: str, error_list: list[ParserError]
    ) -> TranspilationResult:
        try:
            transpiled_sql = transpile(
                sql, read=self.read_dialect, write=write_dialect, pretty=True, error_level=ErrorLevel.RAISE
            )
        except (ParseError, TokenError, UnsupportedError):
            transpiled_sql, error = self.__partial_transpile(write_dialect, sql, file_name, error_list)
            logger.error(f"Exception caught for file {file_name}: {error}")
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
    def safe_parse(statements: str, read: Dialect) -> tuple[list[ParsedExpression], list[str]]:
        dialect = read
        errors = []
        try:
            tokens = dialect.tokenize(sql=statements)
        except TokenError as e:
            error_statement = format_error_message("TOKEN ERROR", e, statements)
            errors.append(error_statement)
            return [], errors

        total = len(tokens)
        chunks: list[list[Token]] = [[]]
        original_sql_chunks: list[str] = []
        current_sql_chunk = []
        # Split tokens into chunks based on semicolons(or other separators)
        # Need to define the separator in Class Tokenizer
        for i, token in enumerate(tokens):
            current_sql_chunk.append(token.text)
            if token.token_type in {TokenType.SEMICOLON}:
                original_sql_chunks.append(" ".join(current_sql_chunk).strip())
                current_sql_chunk = []
                if i < total - 1:
                    chunks.append([])
            else:
                chunks[-1].append(token)

        if current_sql_chunk:
            original_sql_chunks.append("".join(current_sql_chunk).strip())

        parsed_expressions: list[ParsedExpression] = []
        parser_opts = {"error_level": ErrorLevel.RAISE}
        parser = dialect.parser(**parser_opts)
        for i, tokens in enumerate(chunks, start=1):
            original_sql = original_sql_chunks[i - 1]
            try:
                expression = t.cast(
                    list[Expression],
                    parser.parse(tokens),
                )[0]

                parsed_expressions.append(ParsedExpression(expression, original_sql))
            except (ParseError, TokenError, UnsupportedError) as e:
                error_statement = format_error_message("PARSING ERROR", e, original_sql)
                errors.append(error_statement)
            finally:
                parser.reset()
        return parsed_expressions, errors

    @staticmethod
    def _find_root_tables(expression) -> str | None:
        for table in expression.find_all(exp.Table, bfs=False):
            return table.name
        return None

    @staticmethod
    def _handle_errors(
        errors: list[str], error_list: list[ParserError], file_name: str, sql_statements: list[str]
    ) -> list[ParserError]:
        for error in errors:
            sql_statements.append(error)
            error_list.append(ParserError(file_name, refactor_hexadecimal_chars(str(error))))
        return error_list
