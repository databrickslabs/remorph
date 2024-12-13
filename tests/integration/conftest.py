from unittest.mock import create_autospec

import pytest
from pyspark.sql import SparkSession

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam


@pytest.fixture(scope="session")
def mock_spark() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return SparkSession.builder.appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()


@pytest.fixture()
def mock_workspace_client():
    client = create_autospec(WorkspaceClient)
    client.current_user.me = lambda: iam.User(user_name="remorph", groups=[iam.ComplexValue(display="admins")])
    yield client
