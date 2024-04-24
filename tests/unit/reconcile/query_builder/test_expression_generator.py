from sqlglot import expressions as exp

from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    anonymous,
    build_alias,
    build_column,
    build_from_clause,
    build_join_clause,
    build_sub,
    build_threshold_absolute_case,
    build_threshold_percentile_case,
    build_where_clause,
    coalesce,
)
from databricks.labs.remorph.reconcile.recon_config import Thresholds


def test_coalesce():
    col = exp.Column(this="test_column", table="test_table")
    result = col.transform(coalesce)
    assert str(result) == "COALESCE(test_table.test_column, 0)"
    assert isinstance(result, exp.Coalesce)
    assert result.this.this == "test_column"
    assert result.this.table == "test_table"
    assert result.expressions[0].this == "0"


def test_anonymous():
    col = exp.Column(this="test_column", table="test_table")
    result = col.transform(anonymous, "SUM")
    assert str(result) == "SUM(test_table.test_column)"
    assert isinstance(result, exp.Anonymous)
    assert result.this == "SUM"
    assert result.expressions[0].this == "test_column"
    assert result.expressions[0].table == "test_table"


def test_build_column():
    result = build_column("test_column", "test_table")
    assert isinstance(result, exp.Column)
    assert result.this.this == "test_column"
    assert result.table == "test_table"


def test_build_alias():
    result = build_alias("test_column", "test_alias", "test_table")
    assert str(result) == "test_table.test_column AS test_alias"


def test_build_from_clause():
    result = build_from_clause("test_table", "test_alias")
    assert isinstance(result, exp.From)
    assert result.this.this.this == "test_table"
    assert result.this.alias == "test_alias"


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
    assert isinstance(result, exp.Sub)
    assert result.this.this.this == "left_column"
    assert result.this.table == "left_table"
    assert result.expression.this.this == "right_column"
    assert result.expression.table == "right_table"


def test_build_absolute_case():
    threshold = Thresholds(column_name="test_column", lower_bound="5%", upper_bound="-5%", type="float")
    base = exp.Column(this="test_column", table="test_table")
    result = build_threshold_absolute_case(base, threshold)
    assert isinstance(result, exp.Case)


def test_build_percentile_case():
    threshold = Thresholds(column_name="test_column", lower_bound="5%", upper_bound="-5%", type="float")
    base = exp.Column(this="test_column", table="test_table")
    result = build_threshold_percentile_case(base, threshold)
    assert isinstance(result, exp.Case)


def test_build_where_clause():
    where_clause = [
        exp.EQ(
            this=exp.Column(this="test_column", table="test_table"), expression=exp.Literal(this='1', is_string=False)
        )
    ]
    result = build_where_clause(where_clause)
    assert isinstance(result, exp.Or)
