import io
import json
from pathlib import Path
from unittest.mock import create_autospec, patch

import pytest
import yaml
from databricks.labs.blueprint.installation import SerdeError
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph import cli
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.reconcile.recon_config import Table, TableRecon


@pytest.fixture
def mock_workspace_client_cli():
    state = {
        "/Users/foo/.remorph/config.yml": yaml.dump(
            {
                'version': 1,
                'catalog_name': 'transpiler',
                'schema_name': 'remorph',
                'source': 'snowflake',
                'sdk_config': {'cluster_id': 'test_cluster'},
            }
        )
    }

    def download(path: str) -> io.StringIO | io.BytesIO:
        if path not in state:
            raise NotFound(path)
        if ".csv" in path:
            return io.BytesIO(state[path].encode('utf-8'))
        return io.StringIO(state[path])

    workspace_client = create_autospec(WorkspaceClient)
    workspace_client.current_user.me().user_name = "foo"
    workspace_client.workspace.download = download
    return workspace_client


def test_transpile_with_invalid_dialect(mock_workspace_client_cli):
    with pytest.raises(Exception, match="Error: Invalid value for '--source'"):
        cli.transpile(
            mock_workspace_client_cli,
            "invalid_dialect",
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
        pytest.raises(Exception, match="Error: Invalid value for '--skip_validation'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "snowflake",
            "/path/to/sql/file.sql",
            "/path/to/output",
            "invalid_value",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_invalid_input_sql(mock_workspace_client_cli):
    with (
        patch("os.path.exists", return_value=False),
        pytest.raises(Exception, match="Error: Invalid value for '--input_sql'"),
    ):
        cli.transpile(
            mock_workspace_client_cli,
            "snowflake",
            "/path/to/invalid/sql/file.sql",
            "/path/to/output",
            "true",
            "my_catalog",
            "my_schema",
            "current",
        )


def test_transpile_with_valid_input(mock_workspace_client_cli):
    source = "snowflake"
    input_sql = "/path/to/sql/file.sql"
    output_folder = "/path/to/output"
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    mode = "current"
    sdk_config = {'cluster_id': 'test_cluster'}

    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.cli.morph", return_value={}) as mock_morph,
    ):
        cli.transpile(
            mock_workspace_client_cli,
            source,
            input_sql,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )
        mock_morph.assert_called_once_with(
            mock_workspace_client_cli,
            MorphConfig(
                sdk_config=sdk_config,
                source=source,
                input_sql=input_sql,
                output_folder=output_folder,
                skip_validation=True,
                catalog_name=catalog_name,
                schema_name=schema_name,
                mode=mode,
            ),
        )


def test_transpile_empty_output_folder(mock_workspace_client_cli):
    source = "snowflake"
    input_sql = "/path/to/sql/file2.sql"
    output_folder = ""
    skip_validation = "false"
    catalog_name = "my_catalog"
    schema_name = "my_schema"

    mode = "current"
    sdk_config = {'cluster_id': 'test_cluster'}

    with (
        patch("os.path.exists", return_value=True),
        patch("databricks.labs.remorph.cli.morph", return_value={}) as mock_morph,
    ):
        cli.transpile(
            mock_workspace_client_cli,
            source,
            input_sql,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )
        mock_morph.assert_called_once_with(
            mock_workspace_client_cli,
            MorphConfig(
                sdk_config=sdk_config,
                source=source,
                input_sql=input_sql,
                output_folder=None,
                skip_validation=False,
                catalog_name=catalog_name,
                schema_name=schema_name,
                mode=mode,
            ),
        )


def test_transpile_with_incorrect_input_mode(mock_workspace_client_cli):

    with (
        patch("os.path.exists", return_value=True),
        pytest.raises(Exception, match="Error: Invalid value for '--mode':"),
    ):
        source = "snowflake"
        input_sql = "/path/to/sql/file2.sql"
        output_folder = ""
        skip_validation = "false"
        catalog_name = "my_catalog"
        schema_name = "my_schema"
        mode = "preview"

        cli.transpile(
            mock_workspace_client_cli,
            source,
            input_sql,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )


def test_transpile_with_incorrect_input_source(mock_workspace_client_cli):

    with (
        patch("os.path.exists", return_value=True),
        pytest.raises(Exception, match="Error: Invalid value for '--source':"),
    ):
        source = "postgres"
        input_sql = "/path/to/sql/file2.sql"
        output_folder = ""
        skip_validation = "false"
        catalog_name = "my_catalog"
        schema_name = "my_schema"
        mode = "preview"

        cli.transpile(
            mock_workspace_client_cli,
            source,
            input_sql,
            output_folder,
            skip_validation,
            catalog_name,
            schema_name,
            mode,
        )


def test_recon_with_invalid_recon_conf(mock_workspace_client_cli, tmp_path):
    with pytest.raises(Exception, match="Error: Invalid value for '--recon_conf'"):
        invalid_recon_conf_path = tmp_path / "invalid_recon_conf"
        valid_conn_profile_path = tmp_path / "valid_conn_profile"
        valid_conn_profile_path.touch()
        source = "snowflake"
        report = "data"
        cli.reconcile(
            mock_workspace_client_cli,
            str(invalid_recon_conf_path.absolute()),
            str(valid_conn_profile_path.absolute()),
            source,
            report,
        )


def test_recon_with_invalid_conn_profile(mock_workspace_client_cli, tmp_path):
    with pytest.raises(Exception, match="Error: Invalid value for '--conn_profile'"):
        valid_recon_conf_path = tmp_path / "valid_recon_conf"
        valid_recon_conf_path.touch()
        invalid_conn_profile_path = tmp_path / "invalid_conn_profile"
        source = "snowflake"
        report = "data"
        cli.reconcile(
            mock_workspace_client_cli,
            str(valid_recon_conf_path.absolute()),
            str(invalid_conn_profile_path.absolute()),
            source,
            report,
        )


def test_recon_with_invalid_source(mock_workspace_client_cli):
    recon_conf = "/path/to/recon/conf"
    conn_profile = "/path/to/conn/profile"
    source = "invalid_source"
    report = "data"

    with (
        patch("os.path.exists", return_value=True),
        pytest.raises(Exception, match="Error: Invalid value for '--source'"),
    ):
        cli.reconcile(mock_workspace_client_cli, recon_conf, conn_profile, source, report)


def test_recon_with_invalid_report(mock_workspace_client_cli):
    recon_conf = "/path/to/recon/conf"
    conn_profile = "/path/to/conn/profile"
    source = "snowflake"
    report = "invalid_report"

    with (
        patch("os.path.exists", return_value=True),
        pytest.raises(Exception, match="Error: Invalid value for '--report'"),
    ):
        cli.reconcile(mock_workspace_client_cli, recon_conf, conn_profile, source, report)


def test_recon_with_valid_input(mock_workspace_client_cli):
    recon_conf = "/path/to/recon/conf"
    conn_profile = "/path/to/conn/profile"
    source = "snowflake"
    report = "data"

    with patch("os.path.exists", return_value=True), patch("databricks.labs.remorph.cli.recon") as mock_recon:
        cli.reconcile(mock_workspace_client_cli, recon_conf, conn_profile, source, report)
        mock_recon.assert_called_once_with(recon_conf, conn_profile, source, report)


def test_cli_generate_recon_config(mock_workspace_client):
    with patch("databricks.labs.remorph.cli.ReconConfigPrompts") as mock_recon_config:
        cli.generate_recon_config(mock_workspace_client)
        mock_recon_config.assert_called_once_with(mock_workspace_client)


def test_validate_recon_config_with_missing_recon_conf(mock_workspace_client_cli):
    with pytest.raises(Exception, match="No such file or directory: '/path/to/invalid/recon/conf'"):
        invalid_recon_conf_path = "/path/to/invalid/recon/conf"
        cli.validate_recon_config(mock_workspace_client_cli, invalid_recon_conf_path)


def test_validate_recon_config_with_invalid_recon_conf(mock_workspace_client_cli):
    invalid_recon_conf_path = "./recon_conf_test.json"
    recon_config_json = """{
                          source_catalog: "catalog",
                          "source_schema": 'schema',
                          "tables": [
                            ],
                          "target_catalog": "tgt_catalog",
                          "target_schema": "tgt_schema"
                          }"""
    with open(invalid_recon_conf_path, "w", encoding="utf-8") as f:
        f.write(recon_config_json)

    error_msg = "Error: Invalid reconciliation config file .*"

    with patch(
        "databricks.labs.blueprint.installation.Installation.load_local",
        side_effect=json.JSONDecodeError("error", "doc", 0),
    ):
        with pytest.raises(ValueError, match=error_msg):
            cli.validate_recon_config(mock_workspace_client_cli, invalid_recon_conf_path)


def test_validate_recon_config_with_valid_input(mock_workspace_client_cli):
    tables_list = [Table(source_name=field, target_name=field) for field in ("table1", "table2", "table3")]

    table_recon = TableRecon(
        source_catalog="catalog",
        source_schema="schema",
        target_catalog="tgt_catalog",
        target_schema="tgt_schema",
        tables=tables_list,
    )
    recon_config = json.dumps(table_recon, default=vars, indent=2, sort_keys=True)
    recon_config_json = recon_config.replace("null", "None")

    recon_conf = "./recon_conf_test.json"
    with open("./recon_conf_test.json", "w", encoding="utf-8") as f:
        f.write(recon_config_json)

    with pytest.raises(SerdeError, match="source_schema: not a str: value is missing"):
        cli.validate_recon_config(mock_workspace_client_cli, recon_conf)

    Path(recon_conf).unlink()
