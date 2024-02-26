from sqlglot import transpile
from sqlglot.errors import ParseError, TokenError, UnsupportedError

from databricks.labs.remorph.helpers.morph_status import ParserError
from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


class SQLTranspiler:
    def __init__(self, source: str, sql: str, file_nm: str, error_list: list[ParseError]):
        self.source = source
        self.sql = sql
        self.file_nm = file_nm
        self.error_list = error_list

    def transpile(self) -> str:
        if self.source.upper() == "SNOWFLAKE":
            dialect = Snow
        else:
            dialect = self.source.lower()

        try:
            transpiled_sql = transpile(self.sql, read=dialect, write=Databricks, pretty=True, error_level=None)
        except (ParseError, TokenError, UnsupportedError) as e:
            transpiled_sql = ""
            self.error_list.append(ParserError(self.file_nm, e))
        except Exception as er:
            print(er)

        return transpiled_sql
