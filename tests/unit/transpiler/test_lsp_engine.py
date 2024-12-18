import asyncio
from pathlib import Path
from time import sleep

import pytest

from databricks.labs.remorph.errors.exceptions import IllegalStateException
from databricks.labs.remorph.transpiler.lsp.lsp_engine import (
    LSPEngine,
)
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
    for _ in range(1, 10):
        await asyncio.sleep(0.1)
        if lsp_engine.server_has_transpile_capability:
            break
    assert lsp_engine.server_has_transpile_capability


async def test_server_loads_document(lsp_engine, transpile_config):
    sample_path = Path(path_to_resource("lsp_transpiler", "source_stuff.sql"))
    await lsp_engine.initialize(transpile_config)
    lsp_engine.open_document(sample_path)
    log_path = Path(path_to_resource("lsp_transpiler", "test-lsp-server.log"))
    # need to give time to child process
    for _ in range(1, 10):
        await asyncio.sleep(0.1)
        log = log_path.read_text("utf-8")
        if "open-document-uri" in log:
            break
    log = log_path.read_text("utf-8")
    assert f"open-document-uri={sample_path.as_uri()}" in log


async def test_server_closes_document(lsp_engine, transpile_config):
    sample_path = Path(path_to_resource("lsp_transpiler", "source_stuff.sql"))
    await lsp_engine.initialize(transpile_config)
    lsp_engine.open_document(sample_path)
    lsp_engine.close_document(sample_path)
    log_path = Path(path_to_resource("lsp_transpiler", "test-lsp-server.log"))
    # need to give time to child process
    for _ in range(1, 10):
        await asyncio.sleep(0.1)
        log = log_path.read_text("utf-8")
        if "close-document-uri" in log:
            break
    log = log_path.read_text("utf-8")
    assert f"close-document-uri={sample_path.as_uri()}" in log


async def test_server_transpiles_document(lsp_engine, transpile_config):
    sample_path = Path(path_to_resource("lsp_transpiler", "source_stuff.sql"))
    await lsp_engine.initialize(transpile_config)
    lsp_engine.open_document(sample_path)
    response = await lsp_engine.transpile_document(sample_path)
    lsp_engine.close_document(sample_path)
    transpiled_path = Path(path_to_resource("lsp_transpiler", "transpiled_stuff.sql"))
    assert response.changes[0].new_text == transpiled_path.read_text(encoding="utf-8")
