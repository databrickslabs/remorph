import asyncio
import sys
from pathlib import Path
from unit.conftest import path_to_resource

from databricks.labs.blueprint.logger import install_logger
from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine

# this file's sole purpose is to test the LSP Engine's stderr pipe
# it can't be ran as a unit test because pytest captures std i/o
# so this script is a 'manual' test that can be run as required
# it should display the following in red in the console:
"""
Hello there! I'm the client!
17:50:19 ERROR [d.l.r.t.lsp.lsp_engine] Running LSP Test Server...
"""

install_logger()

async def run_lsp_server():
    config_path = path_to_resource("lsp_transpiler", "lsp_config.yml")
    lsp_engine = LSPEngine.from_config_path(Path(config_path))
    config = TranspileConfig(
            transpiler_config_path="whatever",
            source_dialect="snowflake",
            input_source="input_sql",
            output_folder="output_folder",
            sdk_config={"cluster_id": "test_cluster"},
            skip_validation=False,
            catalog_name="catalog",
            schema_name="schema",
        )
    await lsp_engine.initialize(config)
    await asyncio.sleep(5)

if __name__ == "__main__":
    sys.stderr.write("Hello there! I'm the client!\n")
    asyncio.run(run_lsp_server())

