import os
import logging
from pathlib import Path
from unittest.mock import patch

import pytest
from pyspark.sql import SparkSession
from databricks.labs.remorph.__about__ import __version__


logging.getLogger("tests").setLevel("DEBUG")
logging.getLogger("databricks.labs.remorph").setLevel("DEBUG")

logger = logging.getLogger(__name__)


@pytest.fixture
def debug_env_name():
    return "ucws"


@pytest.fixture
def product_info():
    return "remorph", __version__


@pytest.fixture
def get_logger():
    return logger


def pytest_collection_modifyitems(config, items):
    if os.getenv('TEST_ENV') == 'ACCEPTANCE':
        selected_items = []
        deselected_items = []
        # Added only specific tests to run from acceptance.yml
        for item in items:
            if 'tests/integration/reconcile' not in str(item.fspath) and 'tests/unit/' not in str(item.fspath):
                selected_items.append(item)
            else:
                deselected_items.append(item)
        items[:] = selected_items
        config.hook.pytest_deselected(items=deselected_items)


@pytest.fixture(scope="session")
def mock_spark() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return SparkSession.builder.appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()


@pytest.fixture(scope="session")
def mock_credentials():
    with patch(
        'databricks.labs.remorph.connections.credential_manager._load_credentials',
        return_value={
            'secret_vault_type': 'env',
            'secret_vault_name': '',
            'mssql': {
                'user': 'TEST_TSQL_USER',
                'password': 'TEST_TSQL_PASS',
                'server': 'TEST_TSQL_JDBC',
                'database': 'TEST_TSQL_JDBC',
                'driver': 'ODBC Driver 18 for SQL Server',
            },
            'synapse': {
                'workspace': {
                    'name': 'test-workspace',
                    'dedicated_sql_endpoint': 'test-dedicated-endpoint',
                    'serverless_sql_endpoint': 'test-serverless-endpoint',
                    'sql_user': 'test-user',
                    'sql_password': 'test-password',
                    'tz_info': 'UTC',
                },
                'azure_api_access': {
                    'development_endpoint': 'test-dev-endpoint',
                    'azure_client_id': 'test-client-id',
                    'azure_tenant_id': 'test-tenant-id',
                    'azure_client_secret': 'test-client-secret',
                },
                'jdbc': {
                    'auth_type': 'sql_authentication',
                    'fetch_size': '1000',
                    'login_timeout': '30',
                },
                'profiler': {
                    'exclude_serverless_sql_pool': False,
                    'exclude_dedicated_sql_pools': False,
                    'exclude_spark_pools': False,
                    'exclude_monitoring_metrics': False,
                    'redact_sql_pools_sql_text': False,
                },
            },
        },
    ):
        yield


@pytest.fixture
def bladerunner_artifact() -> Path:
    artifact = (
        Path(__file__).parent.parent
        / "resources"
        / "transpiler_configs"
        / "bladerunner"
        / "wheel"
        / "databricks_bb_plugin-0.1.4-py3-none-any.whl"
    )
    assert artifact.exists()
    return artifact


@pytest.fixture
def morpheus_artifact() -> Path:
    artifact = (
        Path(__file__).parent.parent.parent
        / "resources"
        / "transpiler_configs"
        / "morpheus"
        / "jar"
        / "morpheus-lsp-0.2.0-SNAPSHOT-jar-with-dependencies.jar"
    )
    assert artifact.exists()
    return artifact
