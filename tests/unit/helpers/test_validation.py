from databricks.labs.lsql.backends import MockBackend
from databricks.labs.lsql.core import Row
from databricks.labs.remorph.helpers.validation import Validator


def test_valid_query(morph_config):
    query = "SELECT * FROM a_table"
    sql_backend = MockBackend(
        rows={
            "EXPLAIN SELECT": [Row(plan="== Physical Plan ==")],
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.validate_format_result(morph_config, query)
    assert query in result
    assert exception is None


def test_query_with_syntax_error(morph_config):
    query = "SELECT * a_table"
    sql_backend = MockBackend(
        fails_on_first={
            f"EXPLAIN {query}": "[PARSE_SYNTAX_ERROR] Syntax error at",
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.validate_format_result(morph_config, query)
    assert "Exception Start" in result
    assert "Syntax error" in exception


def test_query_with_analysis_error(morph_config):
    error_types = [
        ("[TABLE_OR_VIEW_NOT_FOUND]", True),
        ("[TABLE_OR_VIEW_ALREADY_EXISTS]", True),
        ("[UNRESOLVED_ROUTINE]", False),
        ("Hive support is required to CREATE Hive TABLE (AS SELECT).;", True),
        ("Some other analysis error", False),
    ]

    for err, should_succeed in error_types:
        query = "SELECT * FROM a_table"
        sql_backend = MockBackend(
            fails_on_first={
                f"EXPLAIN {query}": err,
            }
        )
        validator = Validator(sql_backend)
        result, exception = validator.validate_format_result(morph_config, query)
        if should_succeed:
            assert query in result
            assert exception is None
        else:
            assert err in exception


def test_validate_format_result_with_valid_query(morph_config):
    query = "SELECT current_timestamp()"
    sql_backend = MockBackend(
        rows={
            "EXPLAIN SELECT": [Row(plan="== Physical Plan ==")],
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.validate_format_result(morph_config, query)
    assert query in result
    assert exception is None


def test_validate_format_result_with_invalid_query(morph_config):
    query = "SELECT fn() FROM tab"
    sql_backend = MockBackend(
        rows={
            "EXPLAIN SELECT": [
                Row(plan="Error occurred during query planning:"),
                Row(plan="[UNRESOLVED_ROUTINE] Cannot resolve function"),
            ],
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.validate_format_result(morph_config, query)
    assert "Exception Start" in result
    assert "[UNRESOLVED_ROUTINE]" in exception
