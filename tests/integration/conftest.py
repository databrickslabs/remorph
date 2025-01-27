import os
import logging
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

def pytest_collection_modifyitems(config, items):
    if os.getenv('TEST_ENV') == 'ACCEPTANCE':
        selected_items = []
        deselected_items = []
        for item in items:
            if 'tests/integration/connections' in str(item.fspath):
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
