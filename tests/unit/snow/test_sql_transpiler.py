import unittest

from databricks.labs.remorph.helpers.morph_status import ParseError
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler


class TestSQLTranspiler(unittest.TestCase):
    def test_transpile_snowflake(self):
        transpiler = SQLTranspiler("SNOWFLAKE", "SELECT CURRENT_TIMESTAMP(0)", "file.sql", [])
        result = transpiler.transpile()[0]
        self.assertEqual(result, "SELECT\n  CURRENT_TIMESTAMP()")

    def test_transpile_exception(self):
        error_list = [ParseError("", "")]
        transpiler = SQLTranspiler("SNOWFLAKE", "SELECT TRY_TO_NUMBER(COLUMN) FROM table", "file.sql", error_list)
        msg = """Error Parsing args `[Column(\n  this=Identifier(this=COLUMN, quoted=False))]`:
                             * `format` is required
                             * `precision` and `scale` both are required [if specifed]
                          """
        result = transpiler.transpile()
        self.assertEqual(result, "")
        self.assertEqual(error_list[1].file_name, "file.sql")
        self.assertEqual(error_list[1].exception.args[0], msg)
