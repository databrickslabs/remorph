from pathlib import Path

import pytest

from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine
from tests.unit.conftest import path_to_resource


@pytest.fixture
def lsp_engine():
    config_path = path_to_resource("lsp_transpiler", "config.yml")
    return LSPEngine.from_config_path(Path(config_path))

async def test_initializes_lsp_server(lsp_engine):
    await lsp_engine.initialize()
    assert lsp_engine.is_alive
