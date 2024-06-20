from unittest.mock import create_autospec

import pytest
from databricks.labs.blueprint.installation import MockInstallation, Installation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.service import iam

from databricks.labs.remorph.config import (
    MorphConfig,
    RemorphConfigs,
    ReconcileConfig,
    DatabaseConfig,
    ReconcileMetadataConfig,
)
from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.deployment.recon import ReconDeployment


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.current_user.me.side_effect = lambda: iam.User(
        user_name="me@example.com", groups=[iam.ComplexValue(display="admins")]
    )
    return w


def test_demo(ws):
    prompts = MockPrompts(
        {
            r"Enter catalog name": "remorph",
        }
    )
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts)
    recon_deployment = create_autospec(ReconDeployment)
    transpile_config = MorphConfig(
        source="snowflake",
        input_sql="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
        mode="current",
    )
    reconcile_config = ReconcileConfig(
        data_source="oracle",
        report_type="all",
        secret_scope="remorph_oracle",
        database_config=DatabaseConfig(
            source_schema="tpch_sf1000",
            target_catalog="tpch",
            target_schema="1000gb",
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog="remorph",
            schema="reconcile",
            volume="reconcile_volume",
        ),
    )
    config = RemorphConfigs(morph=transpile_config, reconcile=reconcile_config)
    installation = WorkspaceInstallation(ctx, recon_deployment)
    installation.install(config)


def test_no_recon_component_installation(ws):
    ctx = CliContext(ws)
    ctx.replace()
    recon_deployment = create_autospec(ReconDeployment)
    transpile_config = MorphConfig(
        source="snowflake",
        input_sql="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
        mode="current",
    )
    config = RemorphConfigs(morph=transpile_config)
    installation = WorkspaceInstallation(ctx, recon_deployment)
    installation.install(config)
    recon_deployment.install.assert_not_called()


def test_recon_component_installation(ws):
    ctx = CliContext(ws)
    ctx.replace()
    recon_deployment = create_autospec(ReconDeployment)
    reconcile_config = ReconcileConfig(
        data_source="oracle",
        report_type="all",
        secret_scope="remorph_oracle",
        database_config=DatabaseConfig(
            source_schema="tpch_sf1000",
            target_catalog="tpch",
            target_schema="1000gb",
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog="remorph",
            schema="reconcile",
            volume="reconcile_volume",
        ),
    )
    config = RemorphConfigs(reconcile=reconcile_config)
    installation = WorkspaceInstallation(ctx, recon_deployment)
    installation.install(config)
    recon_deployment.install.assert_called()


def test_negative_uninstall_confirmation(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall Remorph .*": "no",
        }
    )
    installation = create_autospec(Installation)
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts, installation=installation)
    recon_deployment = create_autospec(ReconDeployment)
    ws_installation = WorkspaceInstallation(ctx, recon_deployment)
    ws_installation.uninstall()
    installation.remove.assert_not_called()


def test_missing_installation(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall Remorph .*": "yes",
        }
    )
    installation = create_autospec(Installation)
    installation.files.side_effect = NotFound("Installation not found")
    installation.install_folder.return_value = "~/mock"
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts, installation=installation)
    recon_deployment = create_autospec(ReconDeployment)
    ws_installation = WorkspaceInstallation(ctx, recon_deployment)
    ws_installation.uninstall()
    installation.remove.assert_not_called()


def test_uninstall_configs_exist(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall Remorph .*": "yes",
        }
    )
    installation = MockInstallation(
        {
            "config.yml": {
                "source": "snowflake",
                "catalog_name": "transpiler_test",
                "input_sql": "sf_queries",
                "output_folder": "out_dir",
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 1,
            },
            "reconcile.yml": {
                "data_source": "snowflake",
                "report_type": "all",
                "secret_scope": "remorph_snowflake",
                "database_config": {
                    "source_catalog": "snowflake_sample_data",
                    "source_schema": "tpch_sf1000",
                    "target_catalog": "tpch",
                    "target_schema": "1000gb",
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "version": 1,
            },
        }
    )
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts, installation=installation)
    recon_deployment = create_autospec(ReconDeployment)
    ws_installation = WorkspaceInstallation(ctx, recon_deployment)
    ws_installation.uninstall()
    recon_deployment.uninstall.assert_called()
    installation.assert_removed()


def test_uninstall_configs_missing(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall Remorph .*": "yes",
        }
    )
    installation = MockInstallation()
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts, installation=installation)
    recon_deployment = create_autospec(ReconDeployment)
    ws_installation = WorkspaceInstallation(ctx, recon_deployment)
    ws_installation.uninstall()
    recon_deployment.uninstall.assert_not_called()
    installation.assert_removed()
