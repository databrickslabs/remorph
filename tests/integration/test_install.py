import os
import shutil
import sys
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch

import pytest

from databricks.labs.remorph.install import TranspilerInstaller, JarInstaller, PypiInstaller


@pytest.mark.skipif(os.environ.get("CI", "false") == "true", reason="Skipping in CI since we have no installed product")
def test_gets_installed_remorph_version():
    version = TranspilerInstaller.get_installed_version("remorph", False)
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
        sample_wheel = Path(__file__).parent.parent / "resources" / "transpiler_configs" / "rct" / "wheel" / "databricks_labs_remorph_community_transpiler-0.0.1-py3-none-any.whl"
        pip = self._venv / "bin" / "pip3"
        cwd = os.getcwd()
        try:
            os.chdir(self._install_path)
            args = f"'{pip!s}' install '{sample_wheel!s}' -t '{self._site_packages!s}'"
            run(args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=True, check=True)
        finally:
            os.chdir(cwd)

def test_installs_and_runs_rct(patched_transpiler_installer):
    with patch("databricks.labs.remorph.install.PypiInstaller", side_effect=lambda product_name, pypi_name: PatchedPypiInstaller(product_name, pypi_name)):
        patched_transpiler_installer.install_from_pypi("rct", "databricks-labs-remorph-community-transpiler")
        rct = patched_transpiler_installer.transpilers_path() / "rct"
        config = rct / "lib" / "config.yml"
        assert config.exists()
        server = rct / "lib" / "server.py"
        assert server.exists()
        version = rct / "state" / "version.json"
        assert version.exists()
