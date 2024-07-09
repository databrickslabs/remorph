from importlib.resources import files
from unittest.mock import create_autospec

import pytest
from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.lsql.backends import MockBackend
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import (
    InvalidParameterValue,
)
from databricks.sdk.service import jobs
from databricks.sdk.service.workspace import ObjectInfo

import databricks.labs.remorph.resources
from databricks.labs.remorph.config import ReconcileConfig, DatabaseConfig, ReconcileMetadataConfig
from databricks.labs.remorph.helpers.deployment import TableDeployer, JobDeployer

PRODUCT_INFO = ProductInfo.from_class(ReconcileConfig)


@pytest.fixture
def ws():
    workspace_client = create_autospec(WorkspaceClient)
    workspace_client.config.host = "https://foo"
    workspace_client.config.is_aws = True
    workspace_client.config.is_azure = False
    workspace_client.config.is_gcp = False
    workspace_client.workspace.get_status = lambda _: ObjectInfo(object_id=123)
    workspace_client.jobs.create.return_value = jobs.CreateResponse(job_id=123)
    workspace_client.clusters.select_spark_version = lambda **_: "14.2.x-scala2.12"
    workspace_client.clusters.select_node_type = lambda **_: "Standard_F4s"
    return workspace_client


@pytest.fixture
def installation():
    return MockInstallation(is_global=False)


@pytest.fixture
def installation_with_jobs():
    return MockInstallation(
        overwrites={
            'state.json': {
                'resources': {
                    'jobs': {"Remorph_Reconciliation_Job": "123"},
                }
            }
        },
        is_global=False,
    )


@pytest.fixture
def oracle_recon_config() -> ReconcileConfig:
    return ReconcileConfig(
        data_source="oracle",
        report_type="all",
        secret_scope="remorph_oracle9",
        database_config=DatabaseConfig(
            source_schema="tpch_sf10009",
            target_catalog="tpch9",
            target_schema="1000gb9",
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog="remorph9",
            schema="reconcile9",
            volume="reconcile_volume9",
        ),
    )


@pytest.fixture
def snowflake_recon_config() -> ReconcileConfig:
    return ReconcileConfig(
        data_source="snowflake",
        report_type="all",
        secret_scope="remorph_snowflake9",
        database_config=DatabaseConfig(
            source_schema="tpch_sf10009",
            target_catalog="tpch9",
            target_schema="1000gb9",
            source_catalog="snowflake_sample_data9",
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog="remorph9",
            schema="reconcile9",
            volume="reconcile_volume9",
        ),
    )


def test_deploy_recon_table():
    sql_backend = MockBackend()
    table_deployer = TableDeployer(sql_backend, "test_catalog", "test_schema")
    table_name = "main"
    relative_filepath = "queries/reconcile/installation/main.sql"
    expected_query = files(databricks.labs.remorph.resources).joinpath(relative_filepath).read_text()
    table_deployer.deploy_table(table_name, relative_filepath)
    assert expected_query in sql_backend.queries


def test_deploy_job(ws, installation, oracle_recon_config):
    install_state = InstallState.from_installation(installation)
    job_deployer = JobDeployer(ws, installation, install_state, PRODUCT_INFO, oracle_recon_config)
    job_id = job_deployer.deploy_job()
    assert job_id == "123"


def test_deploy_job_with_valid_state(ws, installation_with_jobs, snowflake_recon_config):
    install_state = InstallState.from_installation(installation_with_jobs)
    job_deployer = JobDeployer(ws, installation_with_jobs, install_state, PRODUCT_INFO, snowflake_recon_config)
    job_id = job_deployer.deploy_job()
    assert ws.jobs.reset.called
    assert job_id == "123"


def test_deploy_job_with_invalid_state(ws, installation_with_jobs, snowflake_recon_config):
    install_state = InstallState.from_installation(installation_with_jobs)
    ws.jobs.reset.side_effect = InvalidParameterValue("Job not found")
    job_deployer = JobDeployer(ws, installation_with_jobs, install_state, PRODUCT_INFO, snowflake_recon_config)
    job_id = job_deployer.deploy_job()
    assert ws.jobs.create.called
    assert job_id == "123"


def test_deploy_job_in_test_mode(ws, installation, snowflake_recon_config):
    product_info = create_autospec(ProductInfo)
    product_info.product_name.return_value = "test_product"
    install_state = InstallState.from_installation(installation)
    job_deployer = JobDeployer(ws, installation, install_state, product_info, snowflake_recon_config)
    job_id = job_deployer.deploy_job()
    assert job_id == "123"


def test_deploy_job_in_gcp(ws, installation, snowflake_recon_config):
    ws.config.is_aws = False
    ws.config.is_azure = False
    ws.config.is_gcp = True
    install_state = InstallState.from_installation(installation)
    job_deployer_gcp = JobDeployer(ws, installation, install_state, PRODUCT_INFO, snowflake_recon_config)
    job_id = job_deployer_gcp.deploy_job()
    assert job_id == "123"
