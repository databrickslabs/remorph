from sqlglot import ErrorLevel, exp, parse, transpile
from sqlglot.errors import ParseError, TokenError, UnsupportedError

from databricks.labs.remorph.helpers.morph_status import ParserError
from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


class SQLTranspiler:
    def __init__(self, source: str, error_list: list[ParserError]):
        self.source = source
        self.error_list = error_list
        if self.source.upper() == "SNOWFLAKE":
            self.dialect = Snow
        else:
            self.dialect = self.source.lower()

    def transpile(self, sql: str, file_name: str) -> str:
        try:
            transpiled_sql = transpile(sql, read=self.dialect, write=Databricks, pretty=True, error_level=None)
        except (ParseError, TokenError, UnsupportedError) as e:
            transpiled_sql = ""

            self.error_list.append(ParserError(file_name, e))

        return transpiled_sql

    def parse(self, sql: str, file_name: str) -> exp:
        try:
            expression = parse(sql, read=self.dialect, error_level=ErrorLevel.IMMEDIATE)
        except (ParseError, TokenError, UnsupportedError) as e:
            expression = []
            self.error_list.append(ParserError(file_name, e))

        return expression

    def parse_sql_content(self, sql, file_name):
        parse_error_list = []
        self.error_list = parse_error_list

        parsed_expression = self.parse(sql, file_name)
        for expr in parsed_expression:
            child = str(file_name)
            if expr is not None:
                for create in expr.find_all(exp.Create, exp.Insert, exp.Merge, bfs=False):
                    child = self._find_root_tables(create)

                for select in expr.find_all(exp.Select, exp.Join, exp.With, bfs=False):
                    yield self._find_root_tables(select), child

    @staticmethod
    def _find_root_tables(expression) -> str:
        for table in expression.find_all(exp.Table, bfs=False):
            return table.name
