import asyncio
import re
from pathlib import Path
from typing import Any
from unittest.mock import create_autospec, patch

import pytest

from databricks.connect import DatabricksSession
from databricks.labs.lsql.backends import MockBackend
from databricks.labs.lsql.core import Row
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.config import TranspileConfig, ValidationResult
from databricks.labs.remorph.helpers.validation import Validator
from databricks.labs.remorph.transpiler.execute import (
    transpile as do_transpile,
    transpile_column_exp,
    transpile_sql,
)
from databricks.sdk.core import Config

from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine


# pylint: disable=unspecified-encoding


def transpile(workspace_client: WorkspaceClient, engine: SqlglotEngine, config: TranspileConfig):
    return asyncio.run(do_transpile(workspace_client, engine, config))


def check_status(
    status: dict[str, Any],
    total_files_processed: int,
    total_queries_processed: int,
    analysis_error_count: int,
    parsing_error_count: int,
    validation_error_count: int,
    error_file_name: str,
):
    assert status is not None, "Status returned by transpile function is None"
    assert isinstance(status, dict), "Status returned by transpile function is not a dict"
    assert len(status) > 0, "Status returned by transpile function is an empty dict"
    assert (
        status["total_files_processed"] == total_files_processed
    ), "total_files_processed does not match expected value"
    assert (
        status["total_queries_processed"] == total_queries_processed
    ), "total_queries_processed does not match expected value"
    assert status["analysis_error_count"] == analysis_error_count, "analysis_error_count does not match expected value"

    assert status["parsing_error_count"] == parsing_error_count, "parsing_error_count does not match expected value"
    assert (
        status["validation_error_count"] == validation_error_count
    ), "validation_error_count does not match expected value"
    assert status["error_log_file"], "error_log_file is None or empty"
    assert Path(status["error_log_file"]).name == error_file_name, f"error_log_file does not match {error_file_name}'"


def check_error_lines(error_file_path: str, expected_errors: list[dict[str, str]]):
    pattern = r"TranspileError\(code=(?P<code>[^,]+), kind=(?P<kind>[^,]+), severity=(?P<severity>[^,]+), path='(?P<path>[^']+)', message='(?P<message>[^']+)('\))?"
    with open(Path(error_file_path)) as file:
        error_count = 0
        match_count = 0
        for line in file:
            match = re.match(pattern, line)
            if not match:
                continue
            error_count += 1
            # Extract information using group names from the pattern
            error_info = match.groupdict()
            # Perform assertions
            for expected_error in expected_errors:
                if expected_error["path"] == error_info["path"]:
                    match_count += 1
                    expected_message = expected_error["message"]
                    actual_message = error_info["message"]
                    assert (
                        expected_message in actual_message
                    ), f"Message {actual_message} does not match the expected value {expected_message}"
        assert match_count == len(expected_errors), "Not all expected errors were found"
        assert error_count == match_count, "Not all actual errors were matched"


def test_with_dir_with_output_folder_skipping_validation(
    input_source, output_folder, error_file, mock_workspace_client
):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source),
        output_folder=str(output_folder),
        error_file=str(error_file),
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )
    with patch('databricks.labs.remorph.helpers.db_sql.get_sql_backend', return_value=MockBackend()):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)
    # check the status
    check_status(status, 8, 7, 1, 2, 0, error_file.name)
    # check errors
    expected_errors = [
        {
            "path": f"{input_source!s}/query3.sql",
            "message": f"Unsupported operation found in file {input_source!s}/query3.sql.",
        },
        {"path": f"{input_source!s}/query4.sql", "message": "Parsing error Start:"},
        {"path": f"{input_source!s}/query5.sql", "message": "Token error Start:"},
    ]
    check_error_lines(status["error_log_file"], expected_errors)


def test_with_file(input_source, error_file, mock_workspace_client):
    sdk_config = create_autospec(Config)
    spark = create_autospec(DatabricksSession)
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "query1.sql"),
        output_folder=None,
        error_file=str(error_file),
        sdk_config=sdk_config,
        source_dialect="snowflake",
        skip_validation=False,
    )
    mock_validate = create_autospec(Validator)
    mock_validate.spark = spark
    mock_validate.validate_format_result.return_value = ValidationResult(
        """ Mock validated query """, "Mock validation error"
    )

    with (
        patch(
            'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
            return_value=MockBackend(),
        ),
        patch("databricks.labs.remorph.transpiler.execute.Validator", return_value=mock_validate),
    ):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)

    # check the status
    check_status(status, 1, 1, 0, 0, 1, error_file.name)
    # check errors
    expected_errors = [{"path": f"{input_source!s}/query1.sql", "message": "Mock validation error"}]
    check_error_lines(status["error_log_file"], expected_errors)


def test_with_file_with_output_folder_skip_validation(input_source, output_folder, mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "query1.sql"),
        output_folder=str(output_folder),
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )

    with patch(
        'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
        return_value=MockBackend(),
    ):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)

    # check the status
    check_status(status, 1, 1, 0, 0, 0, "None")


def test_with_not_a_sql_file_skip_validation(input_source, mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "file.txt"),
        output_folder=None,
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )

    with patch(
        'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
        return_value=MockBackend(),
    ):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)

    # check the status
    check_status(status, 0, 0, 0, 0, 0, "None")


def test_with_not_existing_file_skip_validation(input_source, mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "file_not_exist.txt"),
        output_folder=None,
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )
    with pytest.raises(FileNotFoundError):
        with patch(
            'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
            return_value=MockBackend(),
        ):
            transpile(mock_workspace_client, SqlglotEngine(), config)


def test_transpile_sql(mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        source_dialect="snowflake",
        skip_validation=False,
        catalog_name="catalog",
        schema_name="schema",
    )
    query = """select col from table;"""

    with patch(
        'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
        return_value=MockBackend(
            rows={
                "EXPLAIN SELECT": [Row(plan="== Physical Plan ==")],
            }
        ),
    ):
        transpiler_result, validation_result = transpile_sql(mock_workspace_client, config, query)
        assert transpiler_result.transpiled_code == 'SELECT\n  col\nFROM table'
        assert validation_result.exception_msg is None


def test_transpile_column_exp(mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        source_dialect="snowflake",
        skip_validation=True,
        catalog_name="catalog",
        schema_name="schema",
    )
    query = ["case when col1 is null then 1 else 0 end", "col2 * 2", "current_timestamp()"]

    with patch(
        'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
        return_value=MockBackend(
            rows={
                "EXPLAIN SELECT": [Row(plan="== Physical Plan ==")],
            }
        ),
    ):
        result = transpile_column_exp(mock_workspace_client, config, query)
        assert len(result) == 3
        assert result[0][0].transpiled_code == 'CASE WHEN col1 IS NULL THEN 1 ELSE 0 END'
        assert result[1][0].transpiled_code == 'col2 * 2'
        assert result[2][0].transpiled_code == 'CURRENT_TIMESTAMP()'
        assert result[0][0].error_list == []
        assert result[1][0].error_list == []
        assert result[2][0].error_list == []
        assert result[0][1] is None
        assert result[1][1] is None
        assert result[2][1] is None


def test_with_file_with_success(input_source, mock_workspace_client):
    sdk_config = create_autospec(Config)
    spark = create_autospec(DatabricksSession)
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "query1.sql"),
        output_folder=None,
        sdk_config=sdk_config,
        source_dialect="snowflake",
        skip_validation=False,
    )
    mock_validate = create_autospec(Validator)
    mock_validate.spark = spark
    mock_validate.validate_format_result.return_value = ValidationResult(""" Mock validated query """, None)

    with (
        patch(
            'databricks.labs.remorph.helpers.db_sql.get_sql_backend',
            return_value=MockBackend(),
        ),
        patch("databricks.labs.remorph.transpiler.execute.Validator", return_value=mock_validate),
    ):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)
        # assert the status
        check_status(status, 1, 1, 0, 0, 0, "None")


def test_with_input_source_none(mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=None,
        output_folder=None,
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )

    with pytest.raises(ValueError, match="Input SQL path is not provided"):
        transpile(mock_workspace_client, SqlglotEngine(), config)


def test_parse_error_handling(input_source, error_file, mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "query4.sql"),
        output_folder=None,
        error_file=str(error_file),
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )

    with patch('databricks.labs.remorph.helpers.db_sql.get_sql_backend', return_value=MockBackend()):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)

    # assert the status
    check_status(status, 1, 1, 0, 1, 0, error_file.name)
    # check errors
    expected_errors = [{"path": f"{input_source}/query4.sql", "message": "Parsing error Start:"}]
    check_error_lines(status["error_log_file"], expected_errors)


def test_token_error_handling(input_source, error_file, mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=str(input_source / "query5.sql"),
        output_folder=None,
        error_file=str(error_file),
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )

    with patch('databricks.labs.remorph.helpers.db_sql.get_sql_backend', return_value=MockBackend()):
        status, _errors = transpile(mock_workspace_client, SqlglotEngine(), config)
    # assert the status
    check_status(status, 1, 1, 0, 1, 0, error_file.name)
    # check errors
    expected_errors = [{"path": f"{input_source}/query5.sql", "message": "Token error Start:"}]
    check_error_lines(status["error_log_file"], expected_errors)
