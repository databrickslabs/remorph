from collections.abc import Iterable
from pathlib import Path

from sqlglot import expressions as exp, parse, transpile
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression

from databricks.labs.remorph.config import TranspileResult
from databricks.labs.remorph.helpers.file_utils import refactor_hexadecimal_chars
from databricks.labs.remorph.transpiler.sqlglot import lca_utils
from databricks.labs.remorph.transpiler.sqlglot.dialect_utils import SQLGLOT_DIALECTS
from databricks.labs.remorph.transpiler.transpile_status import ParserError, ValidationError, TranspileError
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine


class SqlglotEngine(TranspileEngine):

    @property
    def supported_dialects(self) -> list[str]:
        return sorted(SQLGLOT_DIALECTS.keys())

    def transpile(self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path) -> TranspileResult:
        error: TranspileError | None = self._check_supported(source_dialect, source_code, file_path)
        if error:
            return TranspileResult("", 0, [error])
        try:
            return self._unsafe_transpile(source_dialect, target_dialect, source_code, file_path)
        except (ParseError, TokenError, UnsupportedError) as e:
            error = ParserError(file_path, refactor_hexadecimal_chars(str(e)))
            return TranspileResult("", 0, [error])

    def _unsafe_transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path
    ) -> TranspileResult:
        transpiled_expressions = transpile(
            source_code, read=source_dialect, write=target_dialect, pretty=True, error_level=None
        )
        transpiled_code = "\n".join(transpiled_expressions)
        missing_sqls = list(filter(lambda x: x is None, transpiled_expressions))
        sql_count = len(transpiled_expressions) - len(missing_sqls)
        errors: list[TranspileError] = []
        if missing_sqls:
            error = ParserError(
                file_path,
                f"Skipped {len(missing_sqls)} queries from file {file_path!s}. Check for unsupported operations related to STREAM, TASK, SESSION etc.",
            )
            errors.append(error)
        return TranspileResult(transpiled_code, sql_count, errors)

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

    def analyse_table_lineage(
        self, source_dialect: str, source_code: str, file_path: Path
    ) -> Iterable[tuple[str, str]]:
        parsed_expression, _ = self.parse(source_dialect, source_code, file_path)
        if parsed_expression is not None:
            for expr in parsed_expression:
                child: str = str(file_path)
                if expr is not None:
                    # TODO: fix possible issue where the file reference is lost (if we have a 'create')
                    for change in expr.find_all(exp.Create, exp.Insert, exp.Merge, bfs=False):
                        child = self._find_root_table(change)

                    for query in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                        table = self._find_root_table(query)
                        if table:
                            yield table, child

    @staticmethod
    def _find_root_table(expression) -> str:
        table = expression.find(exp.Table, bfs=False)
        return table.name if table else ""

    def _check_supported(self, source_dialect: str, source_code: str, file_path: Path) -> ValidationError | None:
        return lca_utils.check_for_unsupported_lca(source_dialect, source_code, file_path)
