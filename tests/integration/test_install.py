import os
import shutil
from collections.abc import Iterable
from pathlib import Path

import pytest

from databricks.labs.remorph.install import TranspilerInstaller


@pytest.mark.skipif(os.environ.get("CI", "false") == "true", reason="Skipping in CI since we have no installed product")
def test_gets_installed_version():
    version = TranspilerInstaller.get_installed_version("remorph", False)
    check_valid_version(version)


def test_gets_maven_version():
    version = TranspilerInstaller.get_maven_version("com.databricks", "databricks-connect")
    assert version, "Maybe maven search is down ? (check https://status.maven.org/)"
    check_valid_version(version)


def test_downloads_from_maven(tmp_path: Path) -> None:
    path = tmp_path / "test-download.pom"
    result = TranspilerInstaller.download_from_maven(
        "com.databricks", "databricks-connect", "16.0.0", path, extension="pom"
    )
    assert result == 0
    assert path.exists()
    assert path.stat().st_size == 5_684


@pytest.fixture()
def mock_transpiler_folder(tmp_path: Path) -> Iterable[Path]:
    for transpiler in ("rct", "morpheus"):
        target = tmp_path / transpiler
        target.mkdir()
        target = target / "lib"
        target.mkdir()
        target = target / "config.yml"
        source = TranspilerInstaller.resources_folder() / transpiler / "lib" / "config.yml"
        shutil.copyfile(source, target)
    yield tmp_path


def test_lists_all_transpiler_names(mock_transpiler_folder):
    TranspilerInstaller.transpilers_path = lambda: mock_transpiler_folder
    transpiler_names = TranspilerInstaller.all_transpiler_names()
    assert transpiler_names == {'Morpheus', 'Remorph Community Transpiler'}


def test_lists_all_dialects(mock_transpiler_folder):
    TranspilerInstaller.transpilers_path = lambda: mock_transpiler_folder
    dialects = TranspilerInstaller.all_dialects()
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


def test_lists_dialect_transpilers(mock_transpiler_folder):
    TranspilerInstaller.transpilers_path = lambda: mock_transpiler_folder
    transpilers = TranspilerInstaller.transpilers_with_dialect("snowflake")
    assert transpilers == {'Morpheus', 'Remorph Community Transpiler'}
    transpilers = TranspilerInstaller.transpilers_with_dialect("presto")
    assert transpilers == {'Remorph Community Transpiler'}


def check_valid_version(version: str):
    parts = version.split(".")
    for _, part in enumerate(parts):
        try:
            _ = int(part)
        except ValueError:
            assert False, f"{version} does not look like a valid semver"
