from databricks.labs.lakebridge.reconcile.compare import (
    row_mismatch_flag_columns,
)


def test_row_mismatch_flag_columns_picks_only_genuine_match_triples():
    columns = [
        "id",
        "name_base",
        "name_compare",
        "name_match",
        "acctbal_base",
        "acctbal_compare",
        "acctbal_match",
    ]
    assert row_mismatch_flag_columns(columns) == ["name_match", "acctbal_match"]


def test_row_mismatch_flag_columns_ignores_key_column_named_like_a_flag():
    columns = [
        "order_match",
        "status_base",
        "status_compare",
        "status_match",
    ]
    assert row_mismatch_flag_columns(columns) == ["status_match"]


def test_row_mismatch_flag_columns_handles_compared_column_ending_in_match():
    columns = [
        "id",
        "is_match_base",
        "is_match_compare",
        "is_match_match",
    ]
    assert row_mismatch_flag_columns(columns) == ["is_match_match"]


def test_row_mismatch_flag_columns_empty_when_no_triples():
    assert row_mismatch_flag_columns(["id", "order_match", "name"]) == []
