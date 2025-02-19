import os
import logging
from unittest.mock import patch
from urllib.parse import urlparse
import pytest
from pyspark.sql import SparkSession

from databricks.labs.remorph.connections.credential_manager import create_credential_manager
from databricks.labs.remorph.connections.database_manager import DatabaseManager
from databricks.labs.remorph.__about__ import __version__
from .connections.debug_envgetter import TestEnvGetter


logging.getLogger("tests").setLevel("DEBUG")
logging.getLogger("databricks.labs.remorph").setLevel("DEBUG")

logger = logging.getLogger(__name__)


@pytest.fixture
def debug_env_name():
    return "ucws"


@pytest.fixture
def product_info():
    return "remorph", __version__


def pytest_collection_modifyitems(config, items):
    if os.getenv('TEST_ENV') == 'ACCEPTANCE':
        selected_items = []
        deselected_items = []
        for item in items:
            if 'tests/integration/reconcile' in str(item.fspath):
                deselected_items.append(item)
            else:
                selected_items.append(item)
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
        },
    ):
        yield


@pytest.fixture(scope="module")
def db_manager(mock_credentials):
    env = TestEnvGetter(True)
    config = create_credential_manager("remorph", env).get_credentials("mssql")

    # since the kv has only URL so added explicit parse rules
    base_url, params = config['server'].replace("jdbc:", "", 1).split(";", 1)

    url_parts = urlparse(base_url)
    server = url_parts.hostname
    query_params = dict(param.split("=", 1) for param in params.split(";") if "=" in param)
    database = query_params.get("database", "" "")
    config['server'] = server
    config['database'] = database

    return DatabaseManager("mssql", config)
