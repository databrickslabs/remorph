from pathlib import Path

import pytest
from sqlglot import expressions

from databricks.labs.remorph.transpiler.sqlglot import local_expression
from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine


@pytest.fixture
def transpiler():
    return SqlglotEngine()


def test_transpile_snowflake(transpiler, morph_config):
    transpiler_result = transpiler.transpile("snowflake", morph_config.target_dialect, "SELECT CURRENT_TIMESTAMP(0)", "file.sql", [])
    assert transpiler_result.transpiled_sql[0] == "SELECT\n  CURRENT_TIMESTAMP()"


def test_transpile_exception(transpiler, morph_config):
    transpiler_result = transpiler.transpile("snowflake",
        morph_config.target_dialect, "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27) FROM table", Path("file.sql"), []
    )
    assert transpiler_result.transpiled_sql[0] == ""
    assert transpiler_result.parse_error_list[0].file_path == Path("file.sql")
    assert "Error Parsing args" in transpiler_result.parse_error_list[0].exception


def test_parse_query(transpiler, morph_config):
    parsed_query, _ = transpiler.parse(morph_config.source_dialect, "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27,2) FROM table", Path("file.sql"))

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
    result, error_list = transpiler.parse("snowflake", "invalid sql query", Path("file.sql"))
    assert result is None
    assert error_list.file_path == Path("file.sql")
    assert "Invalid expression / Unexpected token." in error_list.exception


def test_tokenizer_exception(transpiler, morph_config):
    transpiler_result = transpiler.transpile("snowflake", morph_config.target_dialect, "1SELECT ~v\ud83d' ", Path("file.sql"), [])

    assert transpiler_result.transpiled_sql == [""]
    assert transpiler_result.parse_error_list[0].file_path == Path("file.sql")
    assert "Error tokenizing" in transpiler_result.parse_error_list[0].exception


def test_procedure_conversion(transpiler, morph_config):
    procedure_sql = "CREATE OR REPLACE PROCEDURE my_procedure() AS BEGIN SELECT * FROM my_table; END;"
    transpiler_result = transpiler.transpile("databricks", morph_config.target_dialect, procedure_sql, Path("file.sql"), [])
    assert (
        transpiler_result.transpiled_sql[0]
        == "CREATE OR REPLACE PROCEDURE my_procedure() AS BEGIN\nSELECT\n  *\nFROM my_table"
    )


def test_find_root_tables(transpiler):
    expression, _ = transpiler.parse("snowflake", "SELECT * FROM table_name", Path("test.sql"))
    # pylint: disable=protected-access
    assert transpiler._find_root_tables(expression[0]) == "table_name"


def test_parse_sql_content(transpiler):
    result = list(transpiler.parse_sql_content("databricks", "SELECT * FROM table_name", Path("test.sql")))
    assert result[0][0] == "table_name"
    assert result[0][1] == "test.sql"
