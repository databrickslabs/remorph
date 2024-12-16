import asyncio
from pathlib import Path
from time import sleep

import pytest

from databricks.labs.remorph.errors.exceptions import IllegalStateException
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine
from tests.unit.conftest import path_to_resource


@pytest.fixture
def lsp_engine():
    config_path = path_to_resource("lsp_transpiler", "config.yml")
    return LSPEngine.from_config_path(Path(config_path))


async def test_initializes_lsp_server(lsp_engine, transpile_config):
    assert not lsp_engine.is_alive
    await lsp_engine.initialize(transpile_config)
    sleep(3)
    assert lsp_engine.is_alive


async def test_initializes_lsp_server_only_once(lsp_engine, transpile_config):
    await lsp_engine.initialize(transpile_config)
    with pytest.raises(IllegalStateException):
        await lsp_engine.initialize(transpile_config)


async def test_shuts_lsp_server_down(lsp_engine, transpile_config):
    await lsp_engine.initialize(transpile_config)
    await lsp_engine.shutdown()
    assert not lsp_engine.is_alive


async def test_sets_env_variables(lsp_engine, transpile_config):
    await lsp_engine.initialize(transpile_config)
    log = Path(path_to_resource("lsp_transpiler", "test-lsp-server.log")).read_text("utf-8")
    assert "SOME_ENV=abc" in log  # see environment in lsp_transpiler/config.yml


async def test_passes_extra_args(lsp_engine, transpile_config):
    await lsp_engine.initialize(transpile_config)
    log = Path(path_to_resource("lsp_transpiler", "test-lsp-server.log")).read_text("utf-8")
    assert "--stuff=12" in log  # see command_line in lsp_transpiler/config.yml


async def test_receives_config(lsp_engine, transpile_config):
    await lsp_engine.initialize(transpile_config)
    log = Path(path_to_resource("lsp_transpiler", "test-lsp-server.log")).read_text("utf-8")
    assert "dialect=snowflake" in log

async def test_server_has_transpile_capability(lsp_engine, transpile_config):
    await lsp_engine.initialize(transpile_config)
    # need to give time to child process and client listener
    for i in range(1, 10):
        await asyncio.sleep(0.1)
        if lsp_engine.server_has_transpile_capability:
            break
    assert lsp_engine.server_has_transpile_capability
