import asyncio
import re
from pathlib import Path
from typing import Any, cast
from unittest.mock import create_autospec, patch

import pytest

from databricks.labs.lsql.backends import MockBackend
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.helpers.file_utils import dir_walk, is_sql_file
from databricks.labs.remorph.transpiler.execute import transpile as do_transpile


def transpile(workspace_client: WorkspaceClient, config: TranspileConfig):
    engine = create_autospec(TranspileEngine)
    return asyncio.run(do_transpile(workspace_client, engine, config))


def check_status(
    status: dict[str, Any],
    total_files_processed: int,
    total_queries_processed: int,
    analysis_error_count: int,
    parsing_error_count: int,
    validation_error_count: int,
    generation_error_count: int,
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
    assert (
        status["generation_error_count"] == generation_error_count
    ), "generation_error_count does not match expected value"
    assert status["error_log_file"], "error_log_file is None or empty"
    assert Path(status["error_log_file"]).name == error_file_name, f"error_log_file does not match {error_file_name}'"


def check_error_lines(error_file_path: str, expected_errors: list[dict[str, str]]):
    pattern = r"TranspileError\(code=(?P<code>[^,]+), kind=(?P<kind>[^,]+), severity=(?P<severity>[^,]+), path='(?P<path>[^']+)', message='(?P<message>[^']+)('\))?"
    with open(Path(error_file_path), encoding="utf-8") as file:
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


def check_generated(input_source: Path, output_folder: Path):
    for _, _, files in dir_walk(input_source):
        for input_file in files:
            if not is_sql_file(input_file):
                continue
            relative = cast(Path, input_file).relative_to(input_source)
            transpiled = output_folder / relative
            assert transpiled.exists(), f"Could not find transpiled file {transpiled!s} for {input_file!s}"


def test_with_not_a_sql_file(input_source, mock_workspace_client):
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
        status, _errors = transpile(mock_workspace_client, config)

    # check the status
    check_status(status, 0, 0, 0, 0, 0, 0, "None")


def test_with_not_existing_file(input_source, mock_workspace_client):
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
            transpile(mock_workspace_client, config)


def test_with_no_input_source(mock_workspace_client):
    config = TranspileConfig(
        transpiler_config_path="sqlglot",
        input_source=None,
        output_folder=None,
        sdk_config=None,
        source_dialect="snowflake",
        skip_validation=True,
    )

    with pytest.raises(ValueError, match="Input SQL path is not provided"):
        transpile(mock_workspace_client, config)
