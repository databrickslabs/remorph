import logging
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.install import TranspilerInstaller
from databricks.labs.remorph.transpiler.execute import transpile
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine

logger = logging.getLogger(__name__)


# TODO move this test to Bladerunner
async def test_transpiles_informatica_with_sparksql(ws, bladerunner_artifact):
    bladerunner = TranspilerInstaller.transpilers_path() / "bladerunner"
    if bladerunner.exists():
        shutil.rmtree(bladerunner)
    TranspilerInstaller.install_from_pypi("bladerunner", "databricks-bb-plugin", bladerunner_artifact)
    # check execution
    config_path = TranspilerInstaller.transpilers_path() / "bladerunner" / "lib" / "config.yml"
    lsp_engine = LSPEngine.from_config_path(config_path)
    input_source = Path(__file__).parent.parent.parent / "resources" / "functional" / "informatica"
    with TemporaryDirectory() as output_folder:
        transpile_config = TranspileConfig(
            transpiler_config_path=str(config_path),
            source_dialect="informatica (desktop edition)",
            input_source=str(input_source),
            output_folder=output_folder,
            skip_validation=False,
            catalog_name="catalog",
            schema_name="schema",
            transpiler_options={"target-tech": "SPARKSQL"},
        )
        result = await transpile(ws, lsp_engine, transpile_config)
        # purpose was to troubleshoot an issue with transpiler_options
        logger.info(result)
