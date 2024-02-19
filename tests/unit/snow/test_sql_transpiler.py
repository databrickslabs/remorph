from sqlglot import expressions

from databricks.labs.remorph.helpers.morph_status import ParseError
from databricks.labs.remorph.snow import local_expression
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler


def test_transpile_snowflake():
    transpiler = SQLTranspiler("SNOWFLAKE", "SELECT CURRENT_TIMESTAMP(0)", "file.sql", [])
    result = transpiler.transpile()[0]
    assert result == "SELECT\n  CURRENT_TIMESTAMP()"


def test_transpile_exception():
    error_list = [ParseError("", "")]
    transpiler = SQLTranspiler(
        "SNOWFLAKE", "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27) FROM table", "file.sql", error_list
    )
    result = transpiler.transpile()
    assert result == ""
    assert error_list[1].file_name == "file.sql"
    assert "Error Parsing args" in error_list[1].exception.args[0]


def test_parse_query():
    transpiler = SQLTranspiler("SNOWFLAKE", "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27,2) FROM table", "file.sql", [])
    parsed_query = transpiler.parse()

    expected_result = [
        local_expression.TryToNumber(
            this=expressions.Column(this=expressions.Identifier(this="COLUMN", quoted=False)),
            expression=expressions.Parameter(this=expressions.Literal(this=99.99, is_string=False)),
            precision=expressions.Literal(this=27, is_string=False),
            scale=expressions.Literal(this=2, is_string=False),
        )
    ]

    expected_from_result = expressions.From(
        this=expressions.Table(this=expressions.Identifier(this="table", quoted=False))
    )

    for exp in parsed_query:
        if exp:
            assert repr(exp.args["expressions"]) == repr(expected_result)
            assert repr(exp.args["from"]) == repr(expected_from_result)


def test_parse_invalid_query():
    error_list = [ParseError("", "")]
    transpiler = SQLTranspiler("TSQL", "invalid sql query", "file.sql", error_list)
    result = transpiler.parse()
    assert result == []
    assert error_list[1].file_name == "file.sql"
    assert "Invalid expression / Unexpected token." in error_list[1].exception.args[0]
