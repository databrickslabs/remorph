from pathlib import Path
from unittest.mock import create_autospec

from databricks.labs.lsql.backends import MockBackend
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.table import TableDeployment


def test_deploy_table_from_ddl_file():
    ws = create_autospec(WorkspaceClient)
    ctx = CliContext(ws)
    sql_backend = MockBackend()
    ctx.replace(sql_backend=sql_backend)
    table_deployer = TableDeployment(ctx)
    ddl_file = Path(__file__).parent / Path("../../resources/table_deployment_test_query.sql")
    table_deployer.deploy_table_from_ddl_file("catalog", "schema", "table", ddl_file)
    assert len(sql_backend.queries) == 1
    assert sql_backend.queries[0] == ddl_file.read_text()
