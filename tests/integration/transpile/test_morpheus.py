import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.install import TranspilerInstaller
from databricks.labs.remorph.transpiler.execute import transpile
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine


# TODO move this test to Morpheus
async def test_transpiles_all_dbt_project_files(ws):
    morpheus = TranspilerInstaller.transpilers_path() / "morpheus"
    if morpheus.exists():
        shutil.rmtree(morpheus)
    TranspilerInstaller.install_from_maven("morpheus", "com.databricks.labs", "databricks-morph-plugin")
    # check execution
    config_path = morpheus / "lib" / "config.yml"
    lsp_engine = LSPEngine.from_config_path(config_path)
    input_source = Path(__file__).parent.parent.parent / "resources" / "functional" / "dbt"
    with TemporaryDirectory() as output_folder:
        transpile_config = TranspileConfig(
            transpiler_config_path=str(config_path),
            source_dialect="snowflake",
            input_source=str(input_source),
            output_folder=output_folder,
            skip_validation=False,
            catalog_name="catalog",
            schema_name="schema",
        )
        await transpile(ws, lsp_engine, transpile_config)
        assert (Path(output_folder) / "top-query.sql").exists()
        assert (Path(output_folder) / "dbt_project.yml").exists()
        assert (Path(output_folder) / "sub" / "sub-query.sql").exists()
        assert (Path(output_folder) / "sub" / "dbt_project.yml").exists()
        # TODO verify content
