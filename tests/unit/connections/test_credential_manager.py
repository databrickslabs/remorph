import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from databricks.labs.remorph.connections.credential_manager import Credentials
from databricks.labs.remorph.connections.env_getter import EnvGetter
from databricks.labs.blueprint.wheels import ProductInfo
import os


@pytest.fixture
def product_info():
    mock_product_info = MagicMock(spec=ProductInfo)
    mock_product_info.product_name.return_value = "test_product"
    return mock_product_info


@pytest.fixture
def env_getter():
    return MagicMock(spec=EnvGetter)


@pytest.fixture
def local_credentials():
    return {
        'secret_vault_type': 'local',
        'mssql': {
            'database': 'DB_NAME',
            'driver': 'ODBC Driver 18 for SQL Server',
            'server': 'example_host',
            'user': 'local_user',
            'password': 'local_password',
        },
    }


@pytest.fixture
def env_credentials():
    return {
        'secret_vault_type': 'env',
        'mssql': {
            'database': 'DB_NAME',
            'driver': 'ODBC Driver 18 for SQL Server',
            'server': 'example_host',
            'user': 'MSSQL_USER_ENV',
            'password': 'MSSQL_PASSWORD_ENV',
        },
    }


@pytest.fixture
def databricks_credentials():
    return {
        'secret_vault_type': 'databricks',
        'secret_vault_name': 'databricks_vault_name',
        'mssql': {
            'database': 'DB_NAME',
            'driver': 'ODBC Driver 18 for SQL Server',
            'server': 'example_host',
            'user': 'databricks_user',
            'password': 'databricks_password',
        },
    }


@patch('databricks.labs.remorph.connections.credential_manager.Credentials._get_local_version_file_path')
@patch('databricks.labs.remorph.connections.credential_manager.Credentials._load_credentials')
def test_local_credentials(
    mock_load_credentials, mock_get_local_version_file_path, product_info, local_credentials, env_getter
):
    mock_load_credentials.return_value = local_credentials
    mock_get_local_version_file_path.return_value = Path("/fake/path/to/.credentials.yml")
    credentials = Credentials(product_info, env_getter)
    creds = credentials.load('mssql')
    assert creds['user'] == 'local_user'
    assert creds['password'] == 'local_password'


@patch('databricks.labs.remorph.connections.credential_manager.Credentials._get_local_version_file_path')
@patch('databricks.labs.remorph.connections.credential_manager.Credentials._load_credentials')
@patch.dict('os.environ', {'MSSQL_USER_ENV': 'env_user', 'MSSQL_PASSWORD_ENV': 'env_password'})
def test_env_credentials(
    mock_load_credentials, mock_get_local_version_file_path, product_info, env_credentials, env_getter
):
    mock_load_credentials.return_value = env_credentials
    mock_get_local_version_file_path.return_value = Path("/fake/path/to/.credentials.yml")
    env_getter.get.side_effect = lambda key: os.environ[key]
    credentials = Credentials(product_info, env_getter)
    creds = credentials.load('mssql')
    assert creds['user'] == 'env_user'
    assert creds['password'] == 'env_password'


@patch('databricks.labs.remorph.connections.credential_manager.Credentials._get_local_version_file_path')
@patch('databricks.labs.remorph.connections.credential_manager.Credentials._load_credentials')
def test_databricks_credentials(
    mock_load_credentials, mock_get_local_version_file_path, product_info, databricks_credentials, env_getter
):
    mock_load_credentials.return_value = databricks_credentials
    mock_get_local_version_file_path.return_value = Path("/fake/path/to/.credentials.yml")
    credentials = Credentials(product_info, env_getter)
    with pytest.raises(NotImplementedError):
        credentials.load('mssql')
