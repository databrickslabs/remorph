from unittest.mock import patch
from urllib.parse import urlparse

import pytest

from databricks.labs.remorph.connections.credential_manager import create_credential_manager
from databricks.labs.remorph.connections.database_manager import DatabaseManager, MSSQLConnector
from databricks.labs.remorph.discovery.tsql_table_definition import TsqlTableDefinitionService
from integration.connections.debug_envgetter import TestEnvGetter


@pytest.fixture(scope="module")
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


def test_mssql_connector_execute_query(db_manager):
    tss =  TsqlTableDefinitionService(db_manager)
    catalogs = list(tss.get_all_catalog())
    result = db_manager.execute_query(catalogs[0])
    assert result is not None


