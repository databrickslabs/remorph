from unittest.mock import create_autospec

import pytest
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from databricks.sdk.service import iam

from databricks.labs.remorph.config import MorphConfig


@pytest.fixture(scope="session")
def mock_spark_session():
    spark = create_autospec(DatabricksSession)
    yield spark


@pytest.fixture(scope="session")
def mock_databricks_config():
    yield create_autospec(Config)


@pytest.fixture(scope="session")
def mock_workspace_client():
    client = create_autospec(WorkspaceClient)
    client.current_user.me = lambda: iam.User(user_name="remorph", groups=[iam.ComplexValue(display="admins")])
    yield client


@pytest.fixture(scope="session")
def morph_config(mock_databricks_config):
    yield MorphConfig(
        sdk_config=mock_databricks_config,
        source="snowflake",
        input_sql="input_sql",
        output_folder="output_folder",
        skip_validation=False,
        catalog_name="catalog",
        schema_name="schema",
    )
