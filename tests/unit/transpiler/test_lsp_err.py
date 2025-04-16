import asyncio
import logging
from pathlib import Path

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine


async def run_lsp_server():
    config_path = Path(__file__).parent.parent.parent / "resources" / "lsp_transpiler" / "lsp_config.yml"
    lsp_engine = LSPEngine.from_config_path(Path(config_path))
    config = TranspileConfig(
        transpiler_config_path="transpiler_config_path",
        source_dialect="source_dialect",
        input_source="input_source",
    )
    await lsp_engine.initialize(config)


def test_stderr_captured_as_logs(caplog) -> None:
    # The LSP engine logs a message to stderr when it starts. We can verify that stderr is being captured by looking
    # for that log entry.
    with caplog.at_level(logging.ERROR):
        asyncio.run(run_lsp_server())

    expected = (LSPEngine.__module__, logging.ERROR, "Running LSP Test Server...")
    assert expected in caplog.record_tuples
