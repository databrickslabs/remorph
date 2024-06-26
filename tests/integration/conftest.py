import os
from dataclasses import dataclass

import pytest
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import VolumeType

from databricks.labs.remorph.config import ReconcileConfig, DatabaseConfig, ReconcileMetadataConfig, MorphConfig
from databricks.labs.remorph.helpers import db_sql
from databricks.labs.remorph.helpers.deployment import TableDeployer
from databricks.labs.remorph.install import ReconciliationMetadataSetup, CatalogSetup


@dataclass
class TestConfig:
    db_table_catalog: str
    db_table_schema: str
    db_table_name: str
    db_mock_catalog: str
    db_mock_schema: str
    db_mock_src: str
    db_mock_tgt: str
    db_mock_volume: str


@pytest.fixture(scope="session")
def ws():
    # Use variables from Unified Auth
    # See https://databricks-sdk-py.readthedocs.io/en/latest/authentication.html
    product_name, product_version = None, None
    return WorkspaceClient(host=os.environ["DATABRICKS_HOST"], product=product_name, product_version=product_version)


@pytest.fixture(scope="session")
def spark(ws):
    return DatabricksSession.builder.sdkConfig(ws.config).getOrCreate()


@pytest.fixture(scope="module")
def test_config():
    return TestConfig(
        db_table_catalog="samples",
        db_table_schema="tpch",
        db_table_name="lineitem",
        db_mock_catalog="remorph_integration_test",
        db_mock_schema="test",
        db_mock_src="lineitem_src",
        db_mock_tgt="lineitem_tgt",
        db_mock_volume="test_volume",
    )


@pytest.fixture(scope="module")
def reconcile_config(test_config):
    return ReconcileConfig(
        data_source="databricks",
        report_type="all",
        secret_scope="scope_databricks",
        database_config=DatabaseConfig(
            source_schema=test_config.db_mock_schema,
            target_catalog=test_config.db_mock_catalog,
            target_schema=test_config.db_mock_schema,
            source_catalog=test_config.db_mock_catalog,
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog=test_config.db_mock_catalog, schema=test_config.db_mock_schema, volume=test_config.db_mock_volume
        ),
        job_id="1",
        tables=None,
    )


@pytest.fixture(scope="module")
def metrics_deployer(ws, reconcile_config):
    morph_config = MorphConfig(
        source=reconcile_config.data_source,
        catalog_name=reconcile_config.metadata_config.catalog,
        schema_name=reconcile_config.metadata_config.schema,
    )
    sql_backend = db_sql.get_sql_backend(ws, morph_config)
    return TableDeployer(
        sql_backend,
        reconcile_config.metadata_config.catalog,
        reconcile_config.metadata_config.schema,
    )


@pytest.fixture(scope="module")
def setup_teardown(ws, spark, test_config, reconcile_config, metrics_deployer):
    ReconciliationMetadataSetup(ws, reconcile_config, CatalogSetup(ws), metrics_deployer).run()
    _create_reconcile_volume(w=ws, reconcile=reconcile_config)
    yield
    ws.catalogs.delete(name=test_config.db_mock_catalog, force=True)


def _create_reconcile_volume(w, reconcile):
    all_volumes = w.volumes.list(
        reconcile.metadata_config.catalog,
        reconcile.metadata_config.schema,
    )

    reconcile_volume_exists = False
    for volume in all_volumes:
        if volume.name == reconcile.metadata_config.volume:
            reconcile_volume_exists = True
            print("Reconciliation Volume already exists.")
            break

    if not reconcile_volume_exists:
        print("Creating Reconciliation Volume.")
        w.volumes.create(
            reconcile.metadata_config.catalog,
            reconcile.metadata_config.schema,
            reconcile.metadata_config.volume,
            VolumeType.MANAGED,
        )
