from databricks.labs.remorph.helpers.morph_status import ParseError
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler


def test_transpile_snowflake():
    transpiler = SQLTranspiler("SNOWFLAKE", "SELECT CURRENT_TIMESTAMP(0)", "file.sql", [])
    result = transpiler.transpile()[0]
    assert result == "SELECT\n  CURRENT_TIMESTAMP()"


def test_transpile_exception():
    error_list = [ParseError("", "")]
    transpiler = SQLTranspiler("SNOWFLAKE", "SELECT TRY_TO_NUMBER(COLUMN) FROM table", "file.sql", error_list)
    result = transpiler.transpile()
    assert result == ""
    assert error_list[1].file_name == "file.sql"
    assert "Error Parsing args" in error_list[1].exception.args[0]
