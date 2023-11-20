from sqlglot import transpile

from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


class SQLTranspiler:
    def __init__(self, source, sql, file_nm, error_list):
        self.source = source
        self.sql = sql
        self.file_nm = file_nm
        self.error_list = error_list

    def transpile(self):
        if self.source.upper() == "SNOWFLAKE":
            dialect = Snow
        else:
            dialect = self.source.lower()

        try:
            transpiled_sql = transpile(self.sql, read=dialect, write=Databricks, pretty=True, error_level=None)
        except Exception as e:
            transpiled_sql = ""
            self.error_list.append((self.file_nm, e))

        return transpiled_sql
