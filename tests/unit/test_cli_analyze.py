from unittest.mock import create_autospec, patch

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.lakebridge import cli
from databricks.sdk import WorkspaceClient

from databricks.labs.lakebridge.contexts.application import ApplicationContext


def test_analyze():
    prompts = MockPrompts(
        {
            r"Select the source technology": "3",
        }
    )
    with patch.object(ApplicationContext, "prompts", prompts):
        ws = create_autospec(WorkspaceClient)
        cli.analyze(ws, "/tmp/analyzer/snowflake", "/tmp/analyzer/databricks")
