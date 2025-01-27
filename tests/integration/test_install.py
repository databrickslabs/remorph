import os
from pathlib import Path
from tempfile import TemporaryFile

import pytest

from databricks.labs.remorph.install import WorkspaceInstaller


@pytest.mark.skipif(os.environ.get("CI", "false")=="true", reason="Skipping in CI since we have no installed product")
def test_gets_installed_version():
    version = WorkspaceInstaller.get_installed_version("remorph", False)
    check_valid_version(version)

def test_gets_maven_version():
    version = WorkspaceInstaller.get_maven_version("com.databricks", "databricks-connect")
    check_valid_version(version)

def test_downloads_from_maven():
    path = Path(str(TemporaryFile()))
    rc = WorkspaceInstaller.download_from_maven("com.databricks", "databricks-connect", "16.0.0", path, extension="pom")
    assert rc==0
    assert path.exists()
    assert path.stat().st_size == 5_684



def check_valid_version(version: str):
    parts = version.split(".")
    for i in range(0, len(parts)):
        part = parts[i]
        try:
            _ = int(part)
        except:
            assert False, f"{version} does not look like a valid semver"

