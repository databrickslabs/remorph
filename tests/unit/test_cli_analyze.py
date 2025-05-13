from unittest.mock import create_autospec, patch

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph import cli
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.contexts.application import ApplicationContext


def test_analyze_with_missing_installation():
    prompts = MockPrompts(
        {
            r"Enter path to output.*": "/tmp/analyzer/databricks",
            r"Enter path to input.*": "/tmp/analyzer/snowflake",
            r"Select the source technology": "1",
        }
    )
    with patch.object(ApplicationContext, "prompts", prompts):
        ws = create_autospec(WorkspaceClient)
        cli.analyze(ws)
