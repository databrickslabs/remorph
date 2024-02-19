from sqlglot import ErrorLevel, exp, parse, transpile

from databricks.labs.remorph.helpers.morph_status import ParseError
from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


class SQLTranspiler:
    def __init__(self, source: str, sql: str, file_nm: str, error_list: list[ParseError]):
        self.source = source
        self.sql = sql
        self.file_nm = file_nm
        self.error_list = error_list
        if self.source.upper() == "SNOWFLAKE":
            self.dialect = Snow
        else:
            self.dialect = self.source.lower()

    def transpile(self) -> str:

        try:
            transpiled_sql = transpile(self.sql, read=self.dialect, write=Databricks, pretty=True, error_level=None)
        except Exception as e:
            transpiled_sql = ""

            self.error_list.append(ParseError(self.file_nm, e))

        return transpiled_sql

    def parse(self) -> exp:

        try:
            expression = parse(self.sql, read=self.dialect, error_level=ErrorLevel.IMMEDIATE)
        except Exception as e:
            expression = []
            self.error_list.append(ParseError(self.file_nm, e))

        return expression
