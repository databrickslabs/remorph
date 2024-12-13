import pytest
from sqlglot import expressions

from databricks.labs.remorph.transpiler.sqlglot import local_expression
from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine


@pytest.fixture
def transpiler(morph_config):
    read_dialect = morph_config.get_read_dialect()
    return SqlglotEngine(read_dialect)


@pytest.fixture
def write_dialect(morph_config):
    return morph_config.get_write_dialect()


def test_transpile_snowflake(transpiler, write_dialect):
    transpiler_result = transpiler.transpile(write_dialect, "SELECT CURRENT_TIMESTAMP(0)", "file.sql", [])
    assert transpiler_result.transpiled_sql[0] == "SELECT\n  CURRENT_TIMESTAMP()"


def test_transpile_exception(transpiler, write_dialect):
    transpiler_result = transpiler.transpile(
        write_dialect, "SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27) FROM table", "file.sql", []
    )
    assert len(transpiler_result.transpiled_sql) == 1
    assert transpiler_result.parse_error_list[0].file_name == "file.sql"
    assert "Error Parsing args" in transpiler_result.parse_error_list[0].exception


def test_parse_query(transpiler):
    parsed_query, _ = transpiler.parse("SELECT TRY_TO_NUMBER(COLUMN, $99.99, 27,2) FROM table", "file.sql")

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
    result, error_list = transpiler.parse("invalid sql query", "file.sql")
    assert result is None
    assert error_list.file_name == "file.sql"
    assert "Invalid expression / Unexpected token." in error_list.exception


def test_tokenizer_exception(transpiler, write_dialect):
    transpiler_result = transpiler.transpile(write_dialect, "1SELECT ~v\ud83d' ", "file.sql", [])
    assert len(transpiler_result.transpiled_sql) == 1
    assert transpiler_result.parse_error_list[0].file_name == "file.sql"
    assert "Error tokenizing" in transpiler_result.parse_error_list[0].exception


def test_procedure_conversion(transpiler, write_dialect):
    procedure_sql = "CREATE OR REPLACE PROCEDURE my_procedure() AS BEGIN SELECT * FROM my_table; END;"
    transpiler_result = transpiler.transpile(write_dialect, procedure_sql, "file.sql", [])
    assert (
        transpiler_result.transpiled_sql[0]
        == "CREATE OR REPLACE PROCEDURE my_procedure() AS BEGIN\nSELECT\n  *\nFROM my_table"
    )


def test_find_root_tables(transpiler):
    expression, _ = transpiler.parse("SELECT * FROM table_name", "test.sql")
    # pylint: disable=protected-access
    assert transpiler._find_root_tables(expression[0]) == "table_name"


def test_parse_sql_content(transpiler):
    result = list(transpiler.parse_sql_content("SELECT * FROM table_name", "test.sql"))
    assert result[0][0] == "table_name"
    assert result[0][1] == "test.sql"


def test_safe_parse(transpiler, write_dialect):
    dialect = transpiler.read_dialect
    result, error = transpiler.safe_parse("SELECT col1 from tab1;SELECT11 col1 from tab2", dialect)
    expected_result = [expressions.Column(this=expressions.Identifier(this="col1", quoted=False))]
    expected_from_result = expressions.From(
        this=expressions.Table(this=expressions.Identifier(this="tab1", quoted=False))
    )
    for exp in result:
        if exp.parsed_expression:
            print("yes")
            assert repr(exp.parsed_expression.args["expressions"]) == repr(expected_result)
            assert repr(exp.parsed_expression.args["from"]) == repr(expected_from_result)
    assert "PARSING ERROR" in error[0]


def test_safe_parse_with_semicolon(transpiler, write_dialect):
    dialect = transpiler.read_dialect
    result, error = transpiler.safe_parse("SELECT split(col2,';') from tab1 where col1 like ';%'", dialect)
    expected_result = [
        expressions.Split(
            this=expressions.Column(this=expressions.Identifier(this="col2", quoted=False)),
            expression=expressions.Literal(this=";", is_string=True),
        )
    ]
    expected_from_result = expressions.From(
        this=expressions.Table(this=expressions.Identifier(this="tab1", quoted=False))
    )
    expected_where_result = expressions.Where(
        this=expressions.Like(
            this=expressions.Column(this=expressions.Identifier(this="col1", quoted=False)),
            expression=expressions.Literal(this=";%", is_string=True),
        )
    )
    for exp in result:
        if exp.parsed_expression:
            assert repr(exp.parsed_expression.args["expressions"]) == repr(expected_result)
            assert repr(exp.parsed_expression.args["from"]) == repr(expected_from_result)
            assert repr(exp.parsed_expression.args["where"]) == repr(expected_where_result)
    assert len(error) == 0
