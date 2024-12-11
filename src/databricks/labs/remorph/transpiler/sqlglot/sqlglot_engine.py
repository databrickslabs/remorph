from pathlib import Path

from sqlglot import expressions as exp, parse, transpile
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression

from databricks.labs.remorph.config import TranspilationResult
from databricks.labs.remorph.helpers.file_utils import refactor_hexadecimal_chars
from databricks.labs.remorph.transpiler.sqlglot import lca_utils
from databricks.labs.remorph.transpiler.transpile_status import ParserError, ValidationError
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine


class SqlglotEngine(TranspileEngine):

    def transpile(
        self, source_dialect: str, target_dialect: str, source_code: str, file_path: Path, error_list: list[ParserError]
    ) -> TranspilationResult:
        try:
            transpiled_sql = transpile(
                source_code, read=source_dialect, write=target_dialect, pretty=True, error_level=None
            )
        except (ParseError, TokenError, UnsupportedError) as e:
            transpiled_sql = [""]
            error_list.append(ParserError(file_path, refactor_hexadecimal_chars(str(e))))

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

    def analyse_table_lineage(self, source_dialect: str, source_code: str, file_path: Path):
        parsed_expression, _ = self.parse(source_dialect, source_code, file_path)
        if parsed_expression is not None:
            for expr in parsed_expression:
                child: str | None = str(file_path)
                if expr is not None:
                    # TODO: fix possible issue where the file reference is lost (if we have a 'create')
                    for create in expr.find_all(exp.Create, exp.Insert, exp.Merge, bfs=False):
                        child = self._find_root_table(create)

                    for select in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                        yield self._find_root_table(select), child

    @staticmethod
    def _find_root_table(expression) -> str | None:
        table = expression.find_all(exp.Table, bfs=False)
        return table.name if table else None

    def check_for_unsupported_lca(self, source_dialect, source_code, file_path) -> ValidationError | None:
        return lca_utils.check_for_unsupported_lca(source_dialect, source_code, file_path)
