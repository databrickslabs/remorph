import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def mock_spark() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return SparkSession.builder.appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()
