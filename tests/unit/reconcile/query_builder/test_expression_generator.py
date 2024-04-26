from sqlglot import expressions as exp
from sqlglot import parse_one

from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    array_sort,
    array_to_string,
    build_column,
    build_from_clause,
    build_join_clause,
    build_literal,
    build_sub,
    build_threshold_absolute_case,
    build_threshold_percentage_case,
    build_where_clause,
    coalesce,
    json_format,
    sort_array,
    to_char,
    trim,
)
from databricks.labs.remorph.reconcile.recon_config import Thresholds


def test_coalesce(expr):
    assert coalesce(expr, "NA", True).sql() == "SELECT COALESCE(col1, 'NA') FROM DUAL"
    assert coalesce(expr, "0", False).sql() == "SELECT COALESCE(col1, 0) FROM DUAL"
    assert coalesce(expr).sql() == "SELECT COALESCE(col1, 0) FROM DUAL"


def test_trim(expr):
    assert trim(expr).sql() == "SELECT TRIM(col1) FROM DUAL"

    nested_expr = parse_one("select coalesce(col1,' ') FROM DUAL")
    assert trim(nested_expr).sql() == "SELECT COALESCE(TRIM(col1), ' ') FROM DUAL"


def test_json_format():
    expr = parse_one("SELECT col1 FROM DUAL")

    assert json_format(expr).sql() == "SELECT JSON_FORMAT(col1) FROM DUAL"
    assert json_format(expr).sql(dialect="databricks") == "SELECT TO_JSON(col1) FROM DUAL"
    assert json_format(expr).sql(dialect="snowflake") == "SELECT JSON_FORMAT(col1) FROM DUAL"


def test_sort_array(expr):
    assert sort_array(expr).sql() == "SELECT SORT_ARRAY(col1, TRUE) FROM DUAL"
    assert sort_array(expr, asc=False).sql() == "SELECT SORT_ARRAY(col1, FALSE) FROM DUAL"


def test_to_char(expr):
    assert to_char(expr).sql(dialect="oracle") == "SELECT TO_CHAR(col1) FROM DUAL"
    assert to_char(expr, to_format='YYYY-MM-DD').sql(dialect="oracle") == "SELECT TO_CHAR(col1, 'YYYY-MM-DD') FROM DUAL"


def test_array_to_string(expr):
    assert array_to_string(expr).sql() == "SELECT ARRAY_TO_STRING(col1, ',') FROM DUAL"
    assert array_to_string(expr, null_replacement='NA').sql() == "SELECT ARRAY_TO_STRING(col1, ',', 'NA') FROM DUAL"


def test_array_sort(expr):
    assert array_sort(expr).sql() == "SELECT ARRAY_SORT(col1, TRUE) FROM DUAL"
    assert array_sort(expr, asc=False).sql() == "SELECT ARRAY_SORT(col1, FALSE) FROM DUAL"


def test_build_column():
    # test build_column without alias and column as str expr
    assert build_column(this="col1") == exp.Column(this=exp.Identifier(this="col1", quoted=False), table="")

    # test build_column with alias and column as str expr
    assert build_column(this="col1", alias="col1_aliased") == exp.Alias(
        this=exp.Column(this="col1", table=""), alias=exp.Identifier(this="col1_aliased", quoted=False)
    )

    # test build_column with alias and column as exp.Column expr
    assert build_column(
        this=exp.Column(this=exp.Identifier(this="col1", quoted=False), table=""), alias="col1_aliased"
    ) == exp.Alias(
        this=exp.Column(this=exp.Identifier(this="col1", quoted=False), table=""),
        alias=exp.Identifier(this="col1_aliased", quoted=False),
    )

    # with table name
    result = build_column(this="test_column", alias="test_alias", table_name="test_table")
    assert str(result) == "test_table.test_column AS test_alias"


def test_build_literal():
    actual = build_literal(this="abc")
    expected = exp.Literal(this="abc", is_string=True)

    assert actual == expected


def test_build_from_clause():
    # with table alias
    result = build_from_clause("test_table", "test_alias")
    assert str(result) == "FROM test_table AS test_alias"
    assert isinstance(result, exp.From)
    assert result.this.this.this == "test_table"
    assert result.this.alias == "test_alias"

    # without table alias
    result = build_from_clause("test_table")
    assert str(result) == "FROM test_table"


def test_build_join_clause():
    result = build_join_clause("test_table", "test_alias", ["test_column"])
    assert str(result) == (
        "INNER JOIN test_table AS test_alias ON source.test_column IS NOT DISTINCT FROM " "test_alias.test_column"
    )
    assert isinstance(result, exp.Join)
    assert result.this.this.this == "test_table"
    assert result.this.alias == "test_alias"


def test_build_sub():
    result = build_sub("left_column", "left_table", "right_column", "right_table")
    assert str(result) == "left_table.left_column - right_table.right_column"
    assert isinstance(result, exp.Sub)
    assert result.this.this.this == "left_column"
    assert result.this.table == "left_table"
    assert result.expression.this.this == "right_column"
    assert result.expression.table == "right_table"


def test_build_absolute_case():
    threshold = Thresholds(column_name="test_column", lower_bound="5%", upper_bound="-5%", type="float")
    base = exp.Column(this="test_column", table="test_table")
    result = build_threshold_absolute_case(base, threshold)
    assert (
        str(result)
        == """CASE WHEN test_table.test_column = 0 THEN "Match" WHEN test_table.test_column BETWEEN 5 AND -5 THEN "Warning" ELSE "Failed" END"""
    )
    assert isinstance(result, exp.Case)


def test_build_percentage_case():
    threshold = Thresholds(column_name="test_column", lower_bound="5%", upper_bound="-5%", type="float")
    base = exp.Column(this="test_column", table="test_table")
    result = build_threshold_percentage_case(base, threshold)
    assert (
        str(result)
        == """CASE WHEN test_table.test_column = 0 THEN "Match" WHEN (test_table.test_column / CASE WHEN databricks.test_column = 0 OR databricks.test_column IS NULL THEN 1 ELSE databricks.test_column END) * 100 BETWEEN 5 AND -5 THEN "Warning" ELSE "Failed" END"""
    )
    assert isinstance(result, exp.Case)


def test_build_where_clause():
    # or condition
    where_clause = [
        exp.EQ(
            this=exp.Column(this="test_column", table="test_table"), expression=exp.Literal(this='1', is_string=False)
        )
    ]
    result = build_where_clause(where_clause)
    assert str(result) == "(1 = 1 OR 1 = 1) OR test_table.test_column = 1"
    assert isinstance(result, exp.Or)

    # and condition
    where_clause = [
        exp.EQ(
            this=exp.Column(this="test_column", table="test_table"), expression=exp.Literal(this='1', is_string=False)
        )
    ]
    result = build_where_clause(where_clause, "and")
    assert str(result) == "(1 = 1 AND 1 = 1) AND test_table.test_column = 1"
    assert isinstance(result, exp.And)
