import asyncio
from unittest.mock import create_autospec, patch, PropertyMock, ANY, MagicMock

import pytest


from databricks.labs.remorph import cli
from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.transpiler.lsp_engine import LSPEngine
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine
from tests.unit.conftest import path_to_resource


def test_transpile_with_missing_installation():
    workspace_client = create_autospec(WorkspaceClient)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        pytest.raises(SystemExit),
    ):
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = None
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )


def patch_do_transpile():
    mock_transpile = MagicMock(return_value=({}, []))

    @asyncio.coroutine
    def patched_do_transpile(*args, **kwargs):
        return mock_transpile(*args, **kwargs)

    return mock_transpile, patched_do_transpile


def test_transpile_with_no_sdk_config():
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        patch("os.path.exists", return_value=True),
    ):
        default_config = TranspileConfig(
            transpiler_config_path="sqlglot",
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.transpile_config = default_config
        mock_app_context.return_value.workspace_client = workspace_client
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect="snowflake",
                input_source="/path/to/sql/file.sql",
                output_folder="/path/to/output",
                error_file_path="/path/to/errors.log",
                sdk_config=None,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_warehouse_id_in_sdk_config():
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        sdk_config = {"warehouse_id": "w_id"}
        default_config = TranspileConfig(
            transpiler_config_path="sqlglot",
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = default_config
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect="snowflake",
                input_source="/path/to/sql/file.sql",
                output_folder="/path/to/output",
                error_file_path="/path/to/errors.log",
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_cluster_id_in_sdk_config():
    workspace_client = create_autospec(WorkspaceClient)
    mock_transpile, patched_do_transpile = patch_do_transpile()
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        sdk_config = {"cluster_id": "c_id"}
        default_config = TranspileConfig(
            transpiler_config_path="sqlglot",
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            error_file_path="/path/to/errors.log",
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
        )
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = default_config
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect="snowflake",
                input_source="/path/to/sql/file.sql",
                output_folder="/path/to/output",
                error_file_path="/path/to/errors.log",
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
            ),
        )


def test_transpile_with_invalid_transpiler(mock_workspace_client_cli):
    with pytest.raises(Exception, match="Invalid value for '--transpiler-config-path'"):
        cli.transpile(
            mock_workspace_client_cli,
            "sqlglot2",
            "invalid_dialect",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )


def test_transpile_with_invalid_dialect(mock_workspace_client_cli):
    mock_engine = create_autospec(LSPEngine)
    mock_engine.check_source_dialect.side_effect = lambda source_dialect: TranspileEngine.check_source_dialect(mock_engine, source_dialect)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        pytest.raises(Exception, match="Invalid value for '--source-dialect'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "some_transpiler",
            "invalid_dialect",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )


def test_transpile_with_invalid_skip_validation(mock_workspace_client_cli):
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        pytest.raises(Exception, match="Invalid value for '--skip-validation'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "invalid_value",
            "my_catalog",
            "my_schema",
        )


def test_transpile_with_invalid_input_source(mock_workspace_client_cli):
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("os.path.exists", return_value=False),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        pytest.raises(Exception, match="Invalid value for '--input-source'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "sqlglot",
            "snowflake",
            "/path/to/invalid/sql/file.sql",
            "/path/to/output",
            "/path/to/errors.log",
            "true",
            "my_catalog",
            "my_schema",
        )


def test_transpile_with_valid_input(mock_workspace_client_cli):
    transpiler = "sqlglot"
    source_dialect = "snowflake"
    input_source = "/path/to/sql/file.sql"
    output_folder = "/path/to/output"
    error_file = "/path/to/errors.log"
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    sdk_config = {'cluster_id': 'test_cluster'}

    mock_transpile, patched_do_transpile = patch_do_transpile()
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            transpiler,
            source_dialect,
            input_source,
            output_folder,
            error_file,
            skip_validation,
            catalog_name,
            schema_name,
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder=output_folder,
                error_file_path=error_file,
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name=catalog_name,
                schema_name=schema_name,
            ),
        )


def test_transpile_with_valid_transpiler(mock_workspace_client_cli):
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    source_dialect = "snowflake"
    input_source = path_to_resource("lsp_transpiler", "source_stuff.sql")
    output_folder = path_to_resource("lsp_transpiler")
    error_file = ""
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    sdk_config = {'cluster_id': 'test_cluster'}

    mock_transpile, patched_do_transpile = patch_do_transpile()
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            transpiler_config_path,
            source_dialect,
            input_source,
            output_folder,
            error_file,
            skip_validation,
            catalog_name,
            schema_name,
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path=transpiler_config_path,
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder=output_folder,
                error_file_path=error_file,
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name=catalog_name,
                schema_name=schema_name,
            ),
        )


def test_transpile_empty_output_folder(mock_workspace_client_cli):
    transpiler = "sqlglot"
    source_dialect = "snowflake"
    input_source = "/path/to/sql/file2.sql"
    output_folder = ""
    error_file = ""
    skip_validation = "false"
    catalog_name = "my_catalog"
    schema_name = "my_schema"

    sdk_config = {'cluster_id': 'test_cluster'}

    mock_transpile, patched_do_transpile = patch_do_transpile()
    mock_engine = create_autospec(LSPEngine)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.lsp_engine.LSPEngine.from_config_path", return_value=mock_engine),
        patch("databricks.labs.remorph.cli.do_transpile", new=patched_do_transpile),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            transpiler,
            source_dialect,
            input_source,
            output_folder,
            error_file,
            skip_validation,
            catalog_name,
            schema_name,
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path=transpiler,
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder=output_folder,
                error_file_path=error_file,
                sdk_config=sdk_config,
                skip_validation=False,
                catalog_name=catalog_name,
                schema_name=schema_name,
            ),
        )


def test_transpile_prints_errors(capsys, tmp_path, mock_workspace_client_cli):
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    source_dialect = "snowflake"
    input_source = path_to_resource("lsp_transpiler", "unsupported_lca.sql")
    output_folder = str(tmp_path)
    error_file = None
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    cli.transpile(
        mock_workspace_client_cli,
        transpiler_config_path,
        source_dialect,
        input_source,
        output_folder,
        error_file,
        skip_validation,
        catalog_name,
        schema_name,
    )
    captured = capsys.readouterr()
    assert "TranspileError" in captured.out
    assert "UNSUPPORTED_LCA" in captured.out
