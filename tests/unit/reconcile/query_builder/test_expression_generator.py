from collections.abc import Callable

import pytest
from sqlglot import expressions as exp
from sqlglot import parse_one
from sqlglot.expressions import Column

from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    array_sort,
    array_to_string,
    build_column,
    build_literal,
    coalesce,
    concat,
    get_hash_transform,
    json_format,
    lower,
    sha2,
    sort_array,
    to_char,
    trim,
)


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
        this=exp.Column(this="col1", table_name=""), alias=exp.Identifier(this="col1_aliased", quoted=False)
    )

    # test build_column with alias and column as exp.Column expr
    assert build_column(
        this=exp.Column(this=exp.Identifier(this="col1", quoted=False), table=""), alias="col1_aliased"
    ) == exp.Alias(
        this=exp.Column(this=exp.Identifier(this="col1", quoted=False), table=""),
        alias=exp.Identifier(this="col1_aliased", quoted=False),
    )


def test_build_literal():
    actual = build_literal(this="abc")
    expected = exp.Literal(this="abc", is_string=True)

    assert actual == expected


def test_sha2(expr):
    assert sha2(expr, num_bits="256").sql() == "SELECT SHA2(col1, 256) FROM DUAL"
    assert (
        sha2(Column(this="CONCAT(col1,col2,col3)"), num_bits="256", is_expr=True).sql()
        == "SHA2(CONCAT(col1,col2,col3), 256)"
    )


def test_concat():
    exprs = [exp.Expression(this="col1"), exp.Expression(this="col2")]
    assert concat(exprs) == exp.Concat(
        expressions=[exp.Expression(this="col1"), exp.Expression(this="col2")], safe=True
    )


def test_lower(expr):
    assert lower(expr).sql() == "SELECT LOWER(col1) FROM DUAL"
    assert lower(Column(this="CONCAT(col1,col2,col3)"), is_expr=True).sql() == "LOWER(CONCAT(col1,col2,col3))"


def test_get_hash_transform():
    assert isinstance(get_hash_transform("snowflake"), Callable) is True

    with pytest.raises(ValueError):
        get_hash_transform("unknown")
