import logging
import re
from pathlib import Path
from unittest.mock import create_autospec, patch, PropertyMock, ANY, MagicMock

import pytest
import yaml

from databricks.labs.remorph import cli
from databricks.labs.remorph.config import TranspileConfig
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine
from tests.unit.conftest import path_to_resource


@pytest.fixture(name="transpiler_config_path")
def stubbed_transpiler_config_path(tmp_path: Path) -> Path:
    """Path to a stubbed LSP transpiler configuration file."""
    # Refer to LSPConfig.load() for the expected structure; there is no .save() method.
    lsp_configuration = {
        "remorph": {
            "version": 1,
            "name": "Stubbed LSP Transpiler Configuration",
            "dialects": ["snowflake"],
            "command_line": ["/usr/bin/true"],
            "options": [],
        }
    }
    config_path = tmp_path / "lsp_config.yml"
    with config_path.open("w") as f:
        yaml.dump(lsp_configuration, f)
    return config_path


def test_transpile_with_missing_installation(
    caplog, transpiler_config_path: Path, empty_input_source: Path, output_folder: Path
) -> None:
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
        caplog.at_level(logging.WARNING),
    ):
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = None
        cli.transpile(
            w=workspace_client,
            transpiler_config_path=str(transpiler_config_path),
            source_dialect="snowflake",
            input_source=str(empty_input_source),
            output_folder=str(output_folder),
        )

    mock_transpile.assert_called_once()
    warning_messages = [record.message for record in caplog.records if record.levelno == logging.WARNING]
    assert (
        "Missing workspace transpile configuration, use 'install-transpile' to reinstall and configure."
        in warning_messages
    )


def patch_do_transpile():
    mock_transpile = MagicMock(return_value=({}, []))

    async def patched_do_transpile(*args, **kwargs):
        return mock_transpile(*args, **kwargs)

    return mock_transpile, patched_do_transpile


def test_transpile_with_no_sdk_config(
    transpiler_config_path: Path, empty_input_source: Path, output_folder: Path
) -> None:
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        default_config = TranspileConfig(
            transpiler_config_path=str(transpiler_config_path),
            source_dialect="snowflake",
            input_source=str(empty_input_source),
            output_folder=str(output_folder),
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.transpile_config = default_config
        mock_app_context.return_value.workspace_client = workspace_client
        cli.transpile(w=workspace_client)
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path=str(transpiler_config_path),
                source_dialect="snowflake",
                input_source=str(empty_input_source),
                output_folder=str(output_folder),
                error_file_path=None,
                sdk_config=None,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_warehouse_id_in_sdk_config(
    transpiler_config_path: Path, empty_input_source: Path, output_folder: Path
) -> None:
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        sdk_config = {"warehouse_id": "w_id"}
        default_config = TranspileConfig(
            transpiler_config_path=str(transpiler_config_path),
            source_dialect="snowflake",
            input_source=str(empty_input_source),
            output_folder=str(output_folder),
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = default_config
        cli.transpile(w=workspace_client)
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path=str(transpiler_config_path),
                source_dialect="snowflake",
                input_source=str(empty_input_source),
                output_folder=str(output_folder),
                error_file_path=None,
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_cluster_id_in_sdk_config(
    transpiler_config_path: Path, empty_input_source: Path, output_folder: Path
) -> None:
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        sdk_config = {"cluster_id": "c_id"}
        default_config = TranspileConfig(
            transpiler_config_path=str(transpiler_config_path),
            source_dialect="snowflake",
            input_source=str(empty_input_source),
            output_folder=str(output_folder),
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = default_config
        cli.transpile(w=workspace_client)
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path=str(transpiler_config_path),
                source_dialect="snowflake",
                input_source=str(empty_input_source),
                output_folder=str(output_folder),
                error_file_path=None,
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_invalid_transpiler(mock_workspace_client_cli) -> None:
    expected_error = "Invalid path for '--transpiler-config-path', does not exist: sqlglot2"
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        cli.transpile(w=mock_workspace_client_cli, transpiler_config_path="sqlglot2")


def test_transpile_with_invalid_sqlglot_dialect(mock_workspace_client_cli, transpiler_config_path: Path) -> None:
    expected_error = (
        "Unsupported source dialect provided for '--source-dialect': 'invalid_dialect' (supported: snowflake)"
    )
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=str(transpiler_config_path),
            source_dialect="invalid_dialect",
        )


def test_transpile_with_invalid_transpiler_dialect(mock_workspace_client_cli, transpiler_config_path: Path) -> None:
    engine = create_autospec(TranspileEngine)
    type(engine).supported_dialects = PropertyMock(return_value=["pidgin", "oracle"])
    expected_error = (
        "Unsupported source dialect provided for '--source-dialect': 'snowflake' (supported: pidgin, oracle)"
    )
    with (
        patch("databricks.labs.remorph.transpiler.transpile_engine.TranspileEngine.load_engine", return_value=engine),
        pytest.raises(ValueError, match=re.escape(expected_error)),
    ):
        cli.transpile(
            w=mock_workspace_client_cli, transpiler_config_path=str(transpiler_config_path), source_dialect="snowflake"
        )


def test_transpile_with_invalid_skip_validation(mock_workspace_client_cli, transpiler_config_path: Path) -> None:
    expected_error = "Invalid value for '--skip-validation': 'invalid_value' must be 'true' or 'false'."
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=str(transpiler_config_path),
            skip_validation="invalid_value",
        )


def test_transpile_with_invalid_input_source(mock_workspace_client_cli, transpiler_config_path: Path) -> None:
    expected_error = "Invalid path for '--input-source', does not exist: /path/that/does/not/exist"
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=str(transpiler_config_path),
            input_source="/path/that/does/not/exist",
        )


def test_transpile_with_invalid_output_folder(
    mock_workspace_client_cli, transpiler_config_path: Path, empty_input_source: Path
) -> None:
    expected_error = "Invalid path for '--output-folder', parent does not exist: /path/that/does/not/exist"
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=str(transpiler_config_path),
            input_source=str(empty_input_source),
            output_folder="/path/that/does/not/exist",
        )


def test_transpile_with_valid_input(
    mock_workspace_client_cli,
    transpiler_config_path: Path,
    empty_input_source: Path,
    output_folder: Path,
    error_file: Path,
) -> None:
    mock_transpile, patched_do_transpile = patch_do_transpile()
    with patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=str(transpiler_config_path),
            source_dialect="snowflake",
            input_source=str(empty_input_source),
            output_folder=str(output_folder),
            error_file_path=str(error_file),
            skip_validation="true",
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path=str(transpiler_config_path),
                source_dialect="snowflake",
                input_source=str(empty_input_source),
                output_folder=str(output_folder),
                error_file_path=str(error_file),
                sdk_config={'cluster_id': 'test_cluster'},
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_valid_transpiler(mock_workspace_client_cli) -> None:
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    input_source = path_to_resource("functional", "snowflake", "aggregates", "least_1.sql")
    output_folder = path_to_resource("lsp_transpiler")
    mock_transpile, patched_do_transpile = patch_do_transpile()
    with patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=transpiler_config_path,
            source_dialect="snowflake",
            input_source=input_source,
            output_folder=output_folder,
            error_file_path=None,
            skip_validation="true",
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path=transpiler_config_path,
                source_dialect="snowflake",
                input_source=input_source,
                output_folder=output_folder,
                sdk_config={'cluster_id': 'test_cluster'},
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_prints_errors(caplog, mock_workspace_client_cli, output_folder: Path) -> None:
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    input_source = path_to_resource("lsp_transpiler", "unsupported_lca.sql")

    with caplog.at_level("ERROR"):
        cli.transpile(
            w=mock_workspace_client_cli,
            transpiler_config_path=transpiler_config_path,
            source_dialect="snowflake",
            input_source=input_source,
            output_folder=str(output_folder),
            skip_validation="true",
        )

    assert any("TranspileError" in record.message for record in caplog.records)
    assert any("UNSUPPORTED_LCA" in record.message for record in caplog.records)
