import logging
import typing as t
from pathlib import Path

from sqlglot import expressions as exp, parse, transpile, Dialect
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression
from sqlglot.tokens import Token, TokenType

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.helpers.string_utils import format_error_message, refactor_hexadecimal_chars
from databricks.labs.remorph.transpiler.sqlglot import lca_utils
from databricks.labs.remorph.transpiler.sqlglot.dialect_utils import get_dialect
from databricks.labs.remorph.transpiler.transpile_status import ParserError, ValidationError
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine

logger = logging.getLogger(__name__)


class ParsedExpression:
    def __init__(self, expression: exp.Expression, original_sql: str):
        self.parsed_expression = expression
        self.original_sql = original_sql


class SqlglotEngine(TranspileEngine):

    def __partial_transpile(
        self,
        read_dialect: Dialect,
        write_dialect: Dialect,
        source_code: str,
        file_path: Path,
        error_list: list[ParserError],
    ) -> tuple[list[str], list[ParserError]]:
        transpiled_sql_statements = []
        parsed_expressions, errors = self.safe_parse(statements=source_code, read_dialect=read_dialect)
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
        updated_error_list = self._handle_errors(errors, error_list, file_path, transpiled_sql_statements)
        return transpiled_sql_statements, updated_error_list

    def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path, error_list: list[ParserError]
    ) -> TranspilationResult:
        read_dialect = get_dialect(source_dialect)
        write_dialect = get_dialect(target_dialect)
        try:
            transpiled_sql = transpile(
                source_code, read=read_dialect, write=write_dialect, pretty=True, error_level=None
            )
            return TranspilationResult(transpiled_sql, error_list)
        except (ParseError, TokenError, UnsupportedError) as e:
            logger.error(f"Exception caught for file {file_path!s}: {e}")
            transpiled_sql, _ = self.__partial_transpile(
                read_dialect, write_dialect, source_code, file_path, error_list
            )
            return TranspilationResult(transpiled_sql, error_list)

    def parse(
        self, source_dialect: str, source_sql: str, file_path: Path
    ) -> tuple[list[Expression | None] | None, ParserError | None]:
        expression = None
        error = None
        try:
            expression = parse(source_sql, read=source_dialect, error_level=ErrorLevel.IMMEDIATE)
        except (ParseError, TokenError, UnsupportedError) as e:
            error = ParserError(file_path, str(e))

        return expression, error

    def parse_sql_content(self, source_dialect: str, source_code: str, file_path: Path):
        parsed_expression, _ = self.parse(source_dialect, source_code, file_path)
        if parsed_expression is not None:
            for expr in parsed_expression:
                child: str | None = str(file_path)
                if expr is not None:
                    for create in expr.find_all(exp.Create, exp.Insert, exp.Merge, bfs=False):
                        child = self._find_root_tables(create)

                    for select in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                        yield self._find_root_tables(select), child

    @staticmethod
    def safe_parse(statements: str, read_dialect: Dialect) -> tuple[list[ParsedExpression], list[str]]:
        errors = []
        try:
            tokens = read_dialect.tokenize(sql=statements)
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
        parser = read_dialect.parser(**parser_opts)
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
        errors: list[str], error_list: list[ParserError], file_path: Path, sql_statements: list[str]
    ) -> list[ParserError]:
        for error in errors:
            sql_statements.append(error)
            error_list.append(ParserError(file_path, refactor_hexadecimal_chars(str(error))))
        return error_list

    def check_for_unsupported_lca(self, source_dialect, source_code, file_path) -> ValidationError | None:
        return lca_utils.check_for_unsupported_lca(get_dialect(source_dialect), source_code, file_path)
