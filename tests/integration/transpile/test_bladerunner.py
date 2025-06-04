from pathlib import Path

from databricks.labs.remorph.install import TranspilerInstaller


def test_transpiles_informatica_with_sparksql():
    artifact = (
        Path(__file__).parent.parent.parent
        / "resources"
        / "transpiler_configs"
        / "bladerunner"
        / "wheel"
        / "databricks_bb_plugin-0.1.4-py3-none-any.whl"
    )
    assert artifact.exists()
    TranspilerInstaller.install_from_pypi("bladerunner", "databricks-labs-bladerunner", artifact)

