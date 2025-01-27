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


@pytest.fixture(scope="session")
def mock_spark() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return SparkSession.builder.appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()
