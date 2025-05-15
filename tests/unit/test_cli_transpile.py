import dataclasses
import os.path

from unittest.mock import create_autospec, patch, ANY, MagicMock
from pathlib import Path

import pytest

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph import cli, resources
from databricks.labs.remorph.config import TranspileConfig
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.contexts.application import ApplicationContext
from tests.unit.conftest import path_to_resource

TRANSPILERS_PATH = Path(resources.__file__).parent / "transpilers"
RCT_CONFIG_PATH = str(TRANSPILERS_PATH / "rct" / "lib" / "config.yml")

assert os.path.exists(RCT_CONFIG_PATH), f"RCT_CONFIG_PATH is not valid: {RCT_CONFIG_PATH}"

def test_transpile_with_missing_installation():
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        pytest.raises(SystemExit),
    ):
        workspace_client = create_autospec(WorkspaceClient)
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = None
        cli.transpile(
            workspace_client,
            RCT_CONFIG_PATH,
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )


@pytest.fixture
def mock_cli_for_transpile(mock_workspace_client):
    mock_transpile = MagicMock(return_value=({}, []))

    async def do_transpile(*args, **kwargs):
        return mock_transpile(*args, **kwargs)

    prompts = MockPrompts(
        {
            "Do you want to use the experimental.*": "no",
            "Enter output directory": "/path/to/output/folder",
            "Select the source dialect.*": "8",  # snowflake
            "Select the transpiler.*": "1",  # RCT
        }
    )
    mock_app_context = create_autospec(ApplicationContext)
    with (
        patch("os.path.exists", side_effect=lambda path: path != "invalid_path"),
        patch("databricks.labs.remorph.install.TranspilerInstaller.transpilers_path", return_value=TRANSPILERS_PATH),
        patch("databricks.labs.remorph.cli.do_transpile", new=do_transpile),
        patch("databricks.labs.remorph.cli.ApplicationContext", mock_app_context),
    ):
        default_config = TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.workspace_client = mock_workspace_client
        mock_app_context.return_value.prompts = prompts

        def set_default_config(config: TranspileConfig):
            mock_app_context.return_value.transpile_config = config

        set_default_config(default_config)
        yield mock_workspace_client, default_config, set_default_config, mock_transpile
        set_default_config(default_config)


def test_transpile_with_no_sdk_config(mock_cli_for_transpile):
    ws, cfg, set_cfg, do_transpile = mock_cli_for_transpile
    set_cfg(dataclasses.replace(cfg, sdk_config=None))
    cli.transpile(
        ws,
    )
    do_transpile.assert_called_once_with(
        ws,
        ANY,
        TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            transpiler_options={'-experimental': False},
        ),
    )


def test_transpile_with_warehouse_id_in_sdk_config(mock_cli_for_transpile):
    ws, cfg, set_cfg, do_transpile = mock_cli_for_transpile
    sdk_config = {"warehouse_id": "w_id"}
    set_cfg(dataclasses.replace(cfg, sdk_config=sdk_config))
    cli.transpile(
        ws,
    )
    do_transpile.assert_called_once_with(
        ws,
        ANY,
        TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            transpiler_options={'-experimental': False},
        ),
    )


def test_transpile_with_cluster_id_in_sdk_config(mock_cli_for_transpile):
    ws, cfg, set_cfg, do_transpile = mock_cli_for_transpile
    sdk_config = {"cluster_id": "c_id"}
    set_cfg(dataclasses.replace(cfg, sdk_config=sdk_config))
    cli.transpile(
        ws,
    )
    do_transpile.assert_called_once_with(
        ws,
        ANY,
        TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            transpiler_options={'-experimental': False},
        ),
    )


def test_transpile_with_invalid_transpiler_config_path(mock_cli_for_transpile):
    ws, _cfg, _set_cfg, do_transpile = mock_cli_for_transpile
    cli.transpile(
        ws,
        transpiler_config_path="invalid_path",
    )
    do_transpile.assert_called_once_with(
        ws,
        ANY,
        TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            transpiler_options={'-experimental': False},
        ),
    )


def test_transpile_with_invalid_transpiler_dialect(mock_cli_for_transpile):
    ws, _cfg, _set_cfg, do_transpile = mock_cli_for_transpile
    cli.transpile(
        ws,
        source_dialect="invalid_dialect",
    )
    do_transpile.assert_called_once_with(
        ws,
        ANY,
        TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            transpiler_options={'-experimental': False},
        ),
    )


def test_transpile_with_invalid_skip_validation(mock_cli_for_transpile):
    ws, _cfg, _set_cfg, _do_transpile = mock_cli_for_transpile
    with (pytest.raises(Exception, match="Invalid value for '--skip-validation'"),):
        cli.transpile(
            ws,
            skip_validation="invalid_value",
        )


def test_transpile_with_invalid_input_source(mock_cli_for_transpile):
    ws, _cfg, _set_cfg, _do_transpile = mock_cli_for_transpile
    with (pytest.raises(Exception, match="Invalid value for '--input-source'"),):
        cli.transpile(
            ws,
            input_source="invalid_path",
        )


def test_transpile_with_valid_inputs(mock_cli_for_transpile):
    ws, _cfg, _set_cfg, do_transpile = mock_cli_for_transpile
    transpiler = RCT_CONFIG_PATH
    source_dialect = "oracle"
    input_source = "/other/path/to/sql/file.sql"
    output_folder = "/other/path/to/output"
    error_file = "/other/path/to/errors.log"
    skip_validation = "false"
    catalog_name = "other_catalog"
    schema_name = "other_schema"
    cli.transpile(
        ws,
        transpiler,
        source_dialect,
        input_source,
        output_folder,
        error_file,
        skip_validation,
        catalog_name,
        schema_name,
    )
    do_transpile.assert_called_once_with(
        ws,
        ANY,
        TranspileConfig(
            transpiler_config_path=RCT_CONFIG_PATH,
            source_dialect=source_dialect,
            input_source=input_source,
            output_folder=output_folder,
            error_file_path=error_file,
            sdk_config=None,
            skip_validation=False,
            catalog_name=catalog_name,
            schema_name=schema_name,
            transpiler_options={"-experimental": False},
        ),
    )


def test_transpile_with_real_inputs(mock_cli_for_transpile):
    ws, _cfg, _set_cfg, do_transpile = mock_cli_for_transpile
    with patch("os.path.exists", os.path.exists):
        transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
        source_dialect = "snowflake"
        input_source = path_to_resource("functional", "snowflake", "aggregates", "least_1.sql")
        output_folder = path_to_resource("lsp_transpiler")
        error_file_path = path_to_resource("lsp_transpiler", "error.log")
        skip_validation = "true"
        catalog_name = "my_catalog"
        schema_name = "my_schema"
        cli.transpile(
            ws,
            transpiler_config_path=transpiler_config_path,
            source_dialect=source_dialect,
            input_source=input_source,
            output_folder=output_folder,
            error_file_path=error_file_path,
            skip_validation=skip_validation,
            catalog_name=catalog_name,
            schema_name=schema_name,
        )
        do_transpile.assert_called_once_with(
            ws,
            ANY,
            TranspileConfig(
                transpiler_config_path=transpiler_config_path,
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder=output_folder,
                error_file_path=error_file_path,
                sdk_config=None,
                skip_validation=True,
                catalog_name=catalog_name,
                schema_name=schema_name,
                transpiler_options={"-experimental": False},
            ),
        )


def test_transpile_with_no_output_folder(mock_cli_for_transpile):
    ws, cfg, set_cfg, _do_transpile = mock_cli_for_transpile
    set_cfg(dataclasses.replace(cfg, output_folder=None))
    cli.transpile(ws)


def test_transpile_prints_errors(caplog, tmp_path, mock_workspace_client):
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    source_dialect = "snowflake"
    input_source = path_to_resource("lsp_transpiler", "unsupported_lca.sql")
    output_folder = str(tmp_path)
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    prompts = MockPrompts(
        {
            "Do you want to use the experimental.*": "no",
            "Enter error file path.*": "errors.log",
        }
    )
    with (
        caplog.at_level("ERROR"),
        patch("databricks.labs.remorph.contexts.application.ApplicationContext.prompts", new_callable=lambda: prompts),
    ):
        cli.transpile(
            mock_workspace_client,
            transpiler_config_path=transpiler_config_path,
            source_dialect=source_dialect,
            input_source=input_source,
            output_folder=output_folder,
            skip_validation=skip_validation,
            catalog_name=catalog_name,
            schema_name=schema_name,
        )

    assert any("TranspileError" in record.message for record in caplog.records)
    assert any("UNSUPPORTED_LCA" in record.message for record in caplog.records)
