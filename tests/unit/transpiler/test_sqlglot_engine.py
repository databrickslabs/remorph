from pathlib import Path

import pytest
from sqlglot import expressions

from databricks.labs.remorph.transpiler.sqlglot import local_expression
from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine


@pytest.fixture
def transpiler():
    return SqlglotEngine()


def test_transpile_snowflake(transpiler, transpile_config):
    transpiler_result = transpiler.transpile(
        "snowflake", transpile_config.target_dialect, "SELECT CURRENT_TIMESTAMP(0)", Path("file.sql")
    )
    assert transpiler_result.transpiled_code == "SELECT\n  CURRENT_TIMESTAMP()"


def test_transpile_exception(transpiler, transpile_config):
    transpiler_result = transpiler.transpile(
        "snowflake",
        transpile_config.target_dialect,
        "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27) FROM table",
        Path("file.sql")
    )
    assert transpiler_result.transpiled_code == ""
    assert transpiler_result.error_list[0].file_path == Path("file.sql")
    assert "Error Parsing args" in transpiler_result.error_list[0].error_msg


def test_parse_query(transpiler, transpile_config):
    parsed_query, _ = transpiler.parse(
        transpile_config.source_dialect, "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27,2) FROM table", Path("file.sql")
    )

    expected_result = [
        local_expression.TryToNumber(
            this=expressions.Column(this=expressions.Identifier(this="COLUMN", quoted=False)),
            expression=expressions.Parameter(
                this=expressions.Literal(this=99, is_string=False),
                suffix=expressions.Literal(this=0.99, is_string=False),
            ),
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


def test_parse_invalid_query(transpiler):
    result, error = transpiler.parse("snowflake", "invalid sql query", Path("file.sql"))
    assert result is None
    assert error.file_path == Path("file.sql")
    assert "Invalid expression / Unexpected token." in error.error_msg


def test_tokenizer_exception(transpiler, transpile_config):
    transpiler_result = transpiler.transpile(
        "snowflake", transpile_config.target_dialect, "1SELECT ~v\ud83d' ", Path("file.sql")
    )

    assert transpiler_result.transpiled_code == ""
    assert transpiler_result.error_list[0].file_path == Path("file.sql")
    assert "Error tokenizing" in transpiler_result.error_list[0].error_msg


def test_procedure_conversion(transpiler, transpile_config):
    procedure_sql = "CREATE OR REPLACE PROCEDURE my_procedure() AS BEGIN SELECT * FROM my_table; END;"
    transpiler_result = transpiler.transpile(
        "databricks", transpile_config.target_dialect, procedure_sql, Path("file.sql")
    )
    assert (
        transpiler_result.transpiled_code
        == "CREATE OR REPLACE PROCEDURE my_procedure() AS BEGIN\nSELECT\n  *\nFROM my_table\nEND"
    )


def test_find_root_tables(transpiler):
    expression, _ = transpiler.parse("snowflake", "SELECT * FROM table_name", Path("test.sql"))
    # pylint: disable=protected-access
    assert transpiler._find_root_table(expression[0]) == "table_name"


def test_analyse_table_lineage(transpiler):
    result = list(transpiler.analyse_table_lineage("databricks", "SELECT * FROM table_name", Path("test.sql")))
    assert result[0][0] == "table_name"
    assert result[0][1] == "test.sql"
