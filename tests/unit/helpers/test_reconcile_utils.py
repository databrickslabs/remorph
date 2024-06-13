import pytest

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.blueprint.installation import MockInstallation
from databricks.sdk.errors.platform import NotFound

from databricks.labs.remorph.helpers.reconcile_utils import ReconcileUtils
from databricks.sdk.service._internal import Wait
from databricks.sdk.service.jobs import RunNowResponse, Run
from databricks.labs.blueprint.installation import SerdeError


@pytest.fixture
def mock_installation_reconcile():
    return MockInstallation(
        {
            "reconcile.yml": {
                "data_source": "snowflake",
                "database_config": {
                    "source_catalog": "abc",
                    "source_schema": "def",
                    "target_catalog": "tgt",
                    "target_schema": "sch",
                },
                "report_type": "all",
                "secret_scope": "remorph",
                "tables": {
                    "filter_type": "all",
                    "tables_list": ["*"],
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "job_id": "45t34wer32",
                "version": 1,
            },
            "recon_config_snowflake_abc_all.json": {
                "source_catalog": "abc",
                "source_schema": "def",
                "tables": [
                    {
                        "column_mapping": [
                            {"source_name": "p_id", "target_name": "product_id"},
                            {"source_name": "p_name", "target_name": "product_name"},
                        ],
                        "join_columns": ["p_id"],
                        "select_columns": ["p_id", "p_name"],
                        "source_name": "product",
                        "target_name": "product_delta",
                    }
                ],
                "target_catalog": "tgt",
                "target_schema": "sch",
            },
        }
    )


def test_reconcile_utils_run(mock_workspace_client, mock_installation_reconcile, monkeypatch):
    def mock_open(url):
        print(f"Opening URL: {url}")

    monkeypatch.setattr("webbrowser.open", mock_open)

    prompts = MockPrompts(
        {
            r"Would you like to overwrite workspace .*": "no",
            r"Open Job Run URL .*": "yes",
        }
    )

    mock_utils = ReconcileUtils(mock_workspace_client, mock_installation_reconcile, prompts)
    op_response = {
        "run_id": "12345",
        "number_in_job": 0,
        "run_page_url": "https://databricks.com/run/12345",
    }
    run = Run.from_dict({"run_id": "12345"})
    wait = Wait(run, response=RunNowResponse.from_dict(op_response), run_id=op_response['run_id'])

    mock_workspace_client.config.host = "https://dbc.com"
    mock_workspace_client.jobs.run_now.return_value = wait
    assert mock_utils.run()


def test_reconcile_utils_no_reconcile_config(mock_workspace_client):
    mock_utils = ReconcileUtils(mock_workspace_client, MockInstallation({}))
    with pytest.raises(AssertionError, match="Error: Cannot load `reconcile_config`"):
        mock_utils.run()


def test_reconcile_utils_reconcile_config_value_error(mock_workspace_client):
    mock_installation = MockInstallation(
        {
            "reconcile.yml": {
                "database_config": {
                    "source_catalog": "sf",
                    "source_schema": "test",
                    "target_catalog": "hive_metastore",
                    "target_schema": "default",
                },
                "report_type": "all",
                "secret_scope": "remorph_sf",
                "tables": {
                    "filter_type": "all",
                    "tables_list": ["*"],
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "job_id": "56454",
                "version": 1,
            }
        }
    )

    mock_utils = ReconcileUtils(
        mock_workspace_client,
        mock_installation,
    )
    with pytest.raises(AssertionError, match="Error: Cannot load `reconcile_config`"):
        mock_utils.run()


def test_reconcile_utils_no_recon_config(mock_workspace_client):
    mock_installation = MockInstallation(
        {
            "reconcile.yml": {
                "data_source": "snowflake",
                "database_config": {
                    "source_catalog": "sf",
                    "source_schema": "mocked",
                    "target_catalog": "hive",
                    "target_schema": "test",
                },
                "report_type": "exclude",
                "secret_scope": "remorph_snowflake",
                "tables": {
                    "filter_type": "exclude",
                    "tables_list": ["product"],
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "job_id": "089765",
                "version": 1,
            }
        }
    )

    prompts = MockPrompts(
        {
            r"Would you like to overwrite workspace .*": "no",
        }
    )

    mock_utils = ReconcileUtils(mock_workspace_client, mock_installation, prompts)
    with pytest.raises(NotFound, match="recon_config_snowflake_sf_exclude.json"):
        mock_utils.run()


def test_reconcile_utils_recon_config_value_error(mock_workspace_client):
    mock_installation = MockInstallation(
        {
            "reconcile.yml": {
                "data_source": "snowflake",
                "database_config": {
                    "source_catalog": "sf",
                    "source_schema": "test",
                    "target_catalog": "hive_metastore",
                    "target_schema": "default",
                },
                "report_type": "include",
                "secret_scope": "remorph_snowflake",
                "tables": {
                    "filter_type": "all",
                    "tables_list": ["*"],
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "job_id": "8765",
                "version": 1,
            },
            "recon_config_snowflake_sf_include.json": {
                "source_catalog": "sf",
                "source_schema": "test",
                "tables": [
                    {
                        "join_columns": ["p_id"],
                        "select_columns": ["p_id", "p_name"],
                        "source_name": "product",
                        "target_name": "product_delta",
                    }
                ],
                "target_schema": "default",
            },
        }
    )

    prompts = MockPrompts(
        {
            r"Would you like to overwrite workspace .*": "no",
        }
    )

    mock_utils = ReconcileUtils(mock_workspace_client, mock_installation, prompts)
    with pytest.raises(SerdeError, match="target_catalog: not a str: value is missing"):
        mock_utils.run()
