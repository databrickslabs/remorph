import os
import shutil
from pathlib import Path
from tempfile import TemporaryFile, TemporaryDirectory

import pytest

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import TranspileConfig, ReconcileConfig
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.install import TranspilerInstaller, WorkspaceInstaller


@pytest.mark.skipif(os.environ.get("CI", "false") == "true", reason="Skipping in CI since we have no installed product")
def test_gets_installed_version():
    version = TranspilerInstaller.get_installed_version("remorph", False)
    check_valid_version(version)


def test_gets_maven_version():
    version = TranspilerInstaller.get_maven_version("com.databricks", "databricks-connect")
    check_valid_version(version)


def test_downloads_from_maven():
    path = Path(str(TemporaryFile()))
    result = TranspilerInstaller.download_from_maven(
        "com.databricks", "databricks-connect", "16.0.0", path, extension="pom"
    )
    assert result == 0
    assert path.exists()
    assert path.stat().st_size == 5_684


@pytest.fixture()
def mock_transpiler_folder():
    with TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir)
        folder.mkdir(exist_ok=True)
        for transpiler in ("rct", "morpheus"):
            target = folder / transpiler
            target.mkdir(exist_ok=True)
            target = target / "lib"
            target.mkdir(exist_ok=True)
            target = target / "config.yml"
            source = TranspilerInstaller.resources_folder() / transpiler / "lib" / "config.yml"
            shutil.copyfile(str(source), str(target))
        yield folder


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


class _WorkspaceInstaller(WorkspaceInstaller):

    def save_config(self, config: TranspileConfig | ReconcileConfig):
        self._save_config(config)


def test_stores_and_fetches_config(ws):
    prompts = MockPrompts(
        {
            r"Open .* in the browser?": "no",
        }
    )
    context = ApplicationContext(ws)
    installer = _WorkspaceInstaller(
        context.workspace_client,
        prompts,
        context.installation,
        context.install_state,
        context.product_info,
        context.resource_configurator,
        context.workspace_installation,
    )
    config = TranspileConfig(
        transpiler_config_path="some_path",
        source_dialect="some_dialect",
        input_source="some_source",
        output_folder="some_output",
        error_file_path="some_file",
        transpiler_options={"a": "1"},
        sdk_config={"a": "1"},
        skip_validation=True,
        catalog_name="some_catalog",
        schema_name="some_schema",
    )
    installer.save_config(config)
    retrieved = ApplicationContext(ws).transpile_config
    assert retrieved == config
