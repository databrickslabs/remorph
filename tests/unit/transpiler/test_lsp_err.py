import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine


@asynccontextmanager
async def run_lsp_server() -> AsyncGenerator[LSPEngine, None]:
    """Run the LSP server and yield the LSPEngine instance."""
    config_path = Path(__file__).parent.parent.parent / "resources" / "lsp_transpiler" / "lsp_config.yml"
    lsp_engine = LSPEngine.from_config_path(config_path)
    config = TranspileConfig(
        transpiler_config_path="transpiler_config_path",
        source_dialect="source_dialect",
        input_source="input_source",
    )
    await lsp_engine.initialize(config)
    try:
        yield lsp_engine
    finally:
        await lsp_engine.shutdown()


@pytest.mark.asyncio
async def test_stderr_captured_as_logs(caplog) -> None:
    # The LSP engine logs a message to stderr when it starts. We can verify that stderr is being captured and logged
    # by looking for the log entry that matches the stderr message.
    with caplog.at_level(logging.INFO):
        async with run_lsp_server() as lsp_engine:
            assert lsp_engine.is_alive

    expected = (LSPEngine.__module__, logging.INFO, "Running LSP Test Server\u2026")
    assert expected in caplog.record_tuples
