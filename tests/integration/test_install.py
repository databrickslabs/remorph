import os
import shutil
import sys
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch

import pytest
from databricks.labs.remorph.config import TranspileConfig

from databricks.labs.remorph.install import TranspilerInstaller, JarInstaller, PypiInstaller
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine


@pytest.mark.skipif(os.environ.get("CI", "false") == "true", reason="Skipping in CI since we have no installed product")
def test_gets_installed_remorph_version(patched_transpiler_installer):
    version = patched_transpiler_installer.get_installed_version("remorph", False)
    check_valid_version(version)


def test_gets_maven_artifact_version():
    version = JarInstaller.get_maven_artifact_version("com.databricks", "databricks-connect")
    check_valid_version(version)


def test_downloads_from_maven():
    with NamedTemporaryFile() as target:
        path = Path(target.name)
        result = JarInstaller.download_from_maven(
            "com.databricks", "databricks-connect", "16.0.0", path, extension="pom"
        )
        assert result == 0
        assert path.exists()
        assert path.stat().st_size == 5_684


def test_gets_pypi_artifact_version():
    version = PypiInstaller.get_pypi_artifact_version("databricks-labs-remorph")
    check_valid_version(version)


def test_downloads_tar_from_pypi():
    with NamedTemporaryFile() as target:
        path = Path(target.name)
        result = PypiInstaller.download_artifact_from_pypi(
            "databricks-labs-remorph-community-transpiler", "0.0.1", path, extension="tar"
        )
        assert result == 0
        assert path.exists()
        assert path.stat().st_size == 41_656


def test_downloads_whl_from_pypi():
    with NamedTemporaryFile() as target:
        path = Path(target.name)
        result = PypiInstaller.download_artifact_from_pypi(
            "databricks-labs-remorph-community-transpiler", "0.0.1", path
        )
        assert result == 0
        assert path.exists()
        assert path.stat().st_size == 35_270


@pytest.fixture()
def patched_transpiler_installer():
    resources_folder = Path(__file__).parent.parent / "resources" / "transpiler_configs"
    with TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir)
        folder.mkdir(exist_ok=True)
        for transpiler in ("rct", "morpheus"):
            target = folder / transpiler
            target.mkdir(exist_ok=True)
            target = target / "lib"
            target.mkdir(exist_ok=True)
            target = target / "config.yml"
            source = resources_folder / transpiler / "lib" / "config.yml"
            shutil.copyfile(str(source), str(target))
        transpilers_path = TranspilerInstaller.transpilers_path
        TranspilerInstaller.transpilers_path = lambda: folder
        yield TranspilerInstaller
        # couldn't find a way to avoid the below mypy error, any solution is welcome
        # pylint: disable=redefined-variable-type
        TranspilerInstaller.transpilers_path = transpilers_path


def test_lists_all_transpiler_names(patched_transpiler_installer):
    transpiler_names = patched_transpiler_installer.all_transpiler_names()
    assert transpiler_names == {'Morpheus', 'Remorph Community Transpiler'}


def test_lists_all_dialects(patched_transpiler_installer):
    dialects = patched_transpiler_installer.all_dialects()
    assert dialects == {
        "athena",
        "bigquery",
        "mysql",
        "netezza",
        "oracle",
        "postgresql",
        "presto",
        "redshift",
        "snowflake",
        "sqlite",
        "teradata",
        "trino",
        "tsql",
        "vertica",
    }


def test_lists_dialect_transpilers(patched_transpiler_installer):
    transpilers = patched_transpiler_installer.transpilers_with_dialect("snowflake")
    assert transpilers == {'Morpheus', 'Remorph Community Transpiler'}
    transpilers = patched_transpiler_installer.transpilers_with_dialect("presto")
    assert transpilers == {'Remorph Community Transpiler'}


def check_valid_version(version: str):
    parts = version.split(".")
    for _, part in enumerate(parts):
        try:
            _ = int(part)
        except ValueError:
            assert False, f"{version} does not look like a valid semver"


class PatchedPypiInstaller(PypiInstaller):

    def _install_from_pip(self):
        sample_wheel = (
            Path(__file__).parent.parent
            / "resources"
            / "transpiler_configs"
            / "rct"
            / "wheel"
            / "databricks_labs_remorph_community_transpiler-0.0.1-py3-none-any.whl"
        )
        assert sample_wheel.exists()
        pip = self._venv / "bin" / "pip3"
        cwd = os.getcwd()
        try:
            os.chdir(self._install_path)
            args = f"'{pip!s}' install '{sample_wheel!s}' -t '{self._site_packages!s}'"
            run(args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=True, check=True)
        finally:
            os.chdir(cwd)


async def test_installs_and_runs_rct(patched_transpiler_installer):
    with patch(
        "databricks.labs.remorph.install.PypiInstaller",
        # couldn't find a way to NOT use a lambda, any solution is welcome
        # pylint: disable=unnecessary-lambda
        side_effect=lambda product_name, pypi_name: PatchedPypiInstaller(product_name, pypi_name),
    ):
        patched_transpiler_installer.install_from_pypi("rct", "databricks-labs-remorph-community-transpiler")
        # check file-level installation
        rct = patched_transpiler_installer.transpilers_path() / "rct"
        config_path = rct / "lib" / "config.yml"
        assert config_path.exists()
        main_path = rct / "lib" / "main.py"
        assert main_path.exists()
        version_path = rct / "state" / "version.json"
        assert version_path.exists()
        # check execution
        lsp_engine = LSPEngine.from_config_path(config_path)
        with TemporaryDirectory() as input_source:
            with TemporaryDirectory() as output_folder:
                transpile_config = TranspileConfig(
                    transpiler_config_path=str(config_path),
                    transpiler_options={"-experimental": True},
                    source_dialect="snowflake",
                    input_source=input_source,
                    output_folder=output_folder,
                    sdk_config={"cluster_id": "test_cluster"},
                    skip_validation=False,
                    catalog_name="catalog",
                    schema_name="schema",
                )
                await lsp_engine.initialize(transpile_config)
                dialect = transpile_config.source_dialect
                input_file = Path(input_source) / "some_query.sql"
                sql_code = "select * from employees"
                result = await lsp_engine.transpile(dialect, "databricks", sql_code, input_file)
                await lsp_engine.shutdown()
                transpiled = " ".join(s.strip() for s in result.transpiled_code.lower().split("\n"))
                assert transpiled == sql_code
