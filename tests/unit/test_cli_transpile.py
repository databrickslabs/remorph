import asyncio
from unittest.mock import create_autospec, patch, PropertyMock, ANY

import pytest


from databricks.labs.remorph import cli
from databricks.labs.remorph.config import TranspileConfig
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
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_no_sdk_config():
    workspace_client = create_autospec(WorkspaceClient)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])) as mock_transpile,
        patch("os.path.exists", return_value=True),
    ):
        default_config = TranspileConfig(
            transpiler_config_path="sqlglot",
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            sdk_config=None,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            mode="current",
        )
        mock_app_context.return_value.transpile_config = default_config
        mock_app_context.return_value.workspace_client = workspace_client
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect="snowflake",
                input_source="/path/to/sql/file.sql",
                output_folder="/path/to/output",
                sdk_config=None,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
                mode="current",
            ),
        )


def test_transpile_with_warehouse_id_in_sdk_config():
    workspace_client = create_autospec(WorkspaceClient)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])) as mock_transpile,
    ):
        sdk_config = {"warehouse_id": "w_id"}
        default_config = TranspileConfig(
            transpiler_config_path="sqlglot",
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            mode="current",
        )
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = default_config
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect="snowflake",
                input_source="/path/to/sql/file.sql",
                output_folder="/path/to/output",
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
                mode="current",
            ),
        )


def test_transpile_with_cluster_id_in_sdk_config():
    workspace_client = create_autospec(WorkspaceClient)
    with (
        patch("databricks.labs.remorph.cli.ApplicationContext", autospec=True) as mock_app_context,
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])) as mock_transpile,
    ):
        sdk_config = {"cluster_id": "c_id"}
        default_config = TranspileConfig(
            transpiler_config_path="sqlglot",
            source_dialect="snowflake",
            input_source="/path/to/sql/file.sql",
            output_folder="/path/to/output",
            sdk_config=sdk_config,
            skip_validation=True,
            catalog_name="my_catalog",
            schema_name="my_schema",
            mode="current",
        )
        mock_app_context.return_value.workspace_client = workspace_client
        mock_app_context.return_value.transpile_config = default_config
        cli.transpile(
            workspace_client,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )
        mock_transpile.assert_called_once_with(
            workspace_client,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect="snowflake",
                input_source="/path/to/sql/file.sql",
                output_folder="/path/to/output",
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name="my_catalog",
                schema_name="my_schema",
                mode="current",
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
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_invalid_sqlglot_dialect(mock_workspace_client_cli):
    with pytest.raises(Exception, match="Invalid value for '--source-dialect'"):
        cli.transpile(
            mock_workspace_client_cli,
            "sqlglot",
            "invalid_dialect",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_invalid_transpiler_dialect(mock_workspace_client_cli):
    engine = create_autospec(TranspileEngine)
    type(engine).supported_dialects = PropertyMock(return_value=["oracle"])
    engine.check_source_dialect = lambda dialect: TranspileEngine.check_source_dialect(engine, dialect)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.transpile_engine.TranspileEngine.load_engine", return_value=engine),
        pytest.raises(Exception, match="Invalid value for '--source-dialect'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "some_transpiler",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_single_transpiler_dialect(mock_workspace_client_cli):
    engine = create_autospec(TranspileEngine)
    type(engine).supported_dialects = PropertyMock(return_value=["snowflake"])
    engine.check_source_dialect = lambda dialect: TranspileEngine.check_source_dialect(engine, dialect)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.transpile_engine.TranspileEngine.load_engine", return_value=engine),
        patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "some_transpiler",
            "",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_missing_transpiler_dialect(mock_workspace_client_cli):
    engine = create_autospec(TranspileEngine)
    type(engine).supported_dialects = PropertyMock(return_value=["snowflake", "oracle"])
    engine.check_source_dialect = lambda dialect: TranspileEngine.check_source_dialect(engine, dialect)
    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.transpiler.transpile_engine.TranspileEngine.load_engine", return_value=engine),
        pytest.raises(Exception, match="Missing value for '--source-dialect'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "some_transpiler",
            "",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_invalid_skip_validation(mock_workspace_client_cli):
    with (
        patch("os.path.exists", return_value=True),
        pytest.raises(Exception, match="Invalid value for '--skip-validation'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "sqlglot",
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "invalid_value",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_invalid_input_source(mock_workspace_client_cli):
    with (
        patch("os.path.exists", return_value=False),
        pytest.raises(Exception, match="Invalid value for '--input-source'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "sqlglot",
            "snowflake",
            "/path/to/invalid/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_valid_input(mock_workspace_client_cli):
    transpiler = "sqlglot"
    source_dialect = "snowflake"
    input_source = "/path/to/sql/file.sql"
    output_folder = "/path/to/output"
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    mode = "current"
    sdk_config = {'cluster_id': 'test_cluster'}

    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])) as mock_transpile,
    ):
        cli.transpile(
            mock_workspace_client_cli,
            transpiler,
            source_dialect,
            input_source,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path="sqlglot",
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder=output_folder,
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name=catalog_name,
                schema_name=schema_name,
                mode=mode,
            ),
        )


def test_transpile_with_valid_transpiler(mock_workspace_client_cli):
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    source_dialect = "snowflake"
    input_source = path_to_resource("functional", "snowflake", "aggregates", "least_1.sql")
    output_folder = path_to_resource("lsp_transpiler")
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    mode = "current"
    sdk_config = {'cluster_id': 'test_cluster'}

    with (patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])) as mock_transpile,):
        cli.transpile(
            mock_workspace_client_cli,
            transpiler_config_path,
            source_dialect,
            input_source,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path=transpiler_config_path,
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder=output_folder,
                sdk_config=sdk_config,
                skip_validation=True,
                catalog_name=catalog_name,
                schema_name=schema_name,
                mode=mode,
            ),
        )


def test_transpile_empty_output_folder(mock_workspace_client_cli):
    transpiler = "sqlglot"
    source_dialect = "snowflake"
    input_source = "/path/to/sql/file2.sql"
    output_folder = ""
    skip_validation = "false"
    catalog_name = "my_catalog"
    schema_name = "my_schema"

    mode = "current"
    sdk_config = {'cluster_id': 'test_cluster'}

    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.cli.do_transpile", return_value=({}, [])) as mock_transpile,
    ):
        cli.transpile(
            mock_workspace_client_cli,
            transpiler,
            source_dialect,
            input_source,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )
        mock_transpile.assert_called_once_with(
            mock_workspace_client_cli,
            ANY,
            TranspileConfig(
                transpiler_config_path=transpiler,
                source_dialect=source_dialect,
                input_source=input_source,
                output_folder="",
                sdk_config=sdk_config,
                skip_validation=False,
                catalog_name=catalog_name,
                schema_name=schema_name,
                mode=mode,
            ),
        )


def test_transpile_with_invalid_mode(mock_workspace_client_cli):
    with (
        patch("os.path.exists", return_value=True),
        pytest.raises(Exception, match="Invalid value for '--mode':"),
    ):
        transpiler = "sqlglot"
        source_dialect = "snowflake"
        input_source = "/path/to/sql/file2.sql"
        output_folder = ""
        skip_validation = "false"
        catalog_name = "my_catalog"
        schema_name = "my_schema"
        mode = "preview"

        cli.transpile(
            mock_workspace_client_cli,
            transpiler,
            source_dialect,
            input_source,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )


def test_transpile_prints_errors(capsys, tmp_path, mock_workspace_client_cli):
    transpiler_config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    source_dialect = "snowflake"
    input_source = path_to_resource("lsp_transpiler", "unsupported_lca.sql")
    output_folder = str(tmp_path)
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    mode = "current"
    cli.transpile(
        mock_workspace_client_cli,
        transpiler_config_path,
        source_dialect,
        input_source,
        output_folder,
        skip_validation,
        catalog_name,
        schema_name,
        mode,
    )
    captured = capsys.readouterr()
    assert "TranspileError" in captured.out
    assert "UNSUPPORTED_LCA" in captured.out

