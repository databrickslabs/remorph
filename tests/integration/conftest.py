import os
import logging
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
            'snowflake': {
                'server': 'TEST_SNOWFLAKE_JDBC',
                'pem': 'TEST_SNOWFLAKE_PRIVATE_KEY',
                'private_key_path': 'TEST_SNOWFLAKE_KEY_PATH',
                'database': 'TEST_SNOWFLAKE_DB',
                'schema': 'TEST_SNOWFLAKE_SCHEMA',
            },
            'postgres': {
                'user': 'TEST_PG_USER',
                'password': 'TEST_PG_PW',
                'server': 'TEST_PG_JDBC',
                'database': 'TEST_PG_DB',
                'driver': 'PostgreSQL Unicode',
            },
        },
    ):
        yield
