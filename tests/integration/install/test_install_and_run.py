import asyncio
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast
from unittest.mock import patch


from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.install import TranspilerInstaller
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPEngine


def format_transpiled(sql: str) -> str:
    parts = sql.lower().split("\n")
    stripped = [s.strip() for s in parts]
    sql = " ".join(stripped)
    sql = sql.replace(";;", ";")
    return sql


# don't run installers in parallel
installer_lock = asyncio.Lock()
base_cwd = os.getcwd()


async def test_installs_and_runs_local_bladerunner(bladerunner_artifact):
    await installer_lock.acquire()
    os.chdir(base_cwd)
    try:
        # TODO temporary workaround for RecursionError with temp dirs on Windows
        if sys.platform == "win32":
            await _install_and_run_pypi_bladerunner()
        else:
            with TemporaryDirectory() as tmpdir:
                with patch.object(TranspilerInstaller, "labs_path", return_value=Path(tmpdir)):
                    await _install_and_run_local_bladerunner(bladerunner_artifact)
    finally:
        installer_lock.release()


async def _install_and_run_local_bladerunner(bladerunner_artifact: Path):
    # TODO: Test that running with existing install does nothing
    # TODO: Test that running with legacy install upgrades it
    # check new install
    bladerunner = TranspilerInstaller.transpilers_path() / "bladerunner"
    assert not bladerunner.exists()
    # fresh install
    TranspilerInstaller.install_from_pypi("bladerunner", "databricks-bb-plugin", bladerunner_artifact)
    # check file-level installation
    config_path = bladerunner / "lib" / "config.yml"
    assert config_path.exists()
    version_path = bladerunner / "state" / "version.json"
    assert version_path.exists()
    # check execution
    lsp_engine = LSPEngine.from_config_path(config_path)
    with TemporaryDirectory() as input_source:
        with TemporaryDirectory() as output_folder:
            transpile_config = TranspileConfig(
                transpiler_config_path=str(config_path),
                source_dialect="oracle",
                input_source=input_source,
                output_folder=output_folder,
                sdk_config={"cluster_id": "test_cluster"},
                skip_validation=False,
                catalog_name="catalog",
                schema_name="schema",
            )
            await lsp_engine.initialize(transpile_config)
            dialect = cast(str, transpile_config.source_dialect)
            input_file = Path(input_source) / "some_query.sql"
            sql_code = "select * from employees"
            result = await lsp_engine.transpile(dialect, "databricks", sql_code, input_file)
            await lsp_engine.shutdown()
            transpiled = format_transpiled(result.transpiled_code)
            assert transpiled == sql_code


async def test_installs_and_runs_pypi_bladerunner():
    await installer_lock.acquire()
    os.chdir(base_cwd)
    try:
        # TODO temporary workaround for RecursionError with temp dirs on Windows
        if sys.platform == "win32":
            await _install_and_run_pypi_bladerunner()
        else:
            with TemporaryDirectory() as tmpdir:
                with patch.object(TranspilerInstaller, "labs_path", return_value=Path(tmpdir)):
                    await _install_and_run_pypi_bladerunner()
    finally:
        installer_lock.release()


async def _install_and_run_pypi_bladerunner():
    # TODO: Test that running with existing install does nothing
    # TODO: Test that running with legacy install upgrades it
    # check new install
    bladerunner = TranspilerInstaller.transpilers_path() / "bladerunner"
    assert not bladerunner.exists()
    # fresh install
    TranspilerInstaller.install_from_pypi("bladerunner", "databricks-bb-plugin")
    # check file-level installation
    config_path = bladerunner / "lib" / "config.yml"
    assert config_path.exists()
    version_path = bladerunner / "state" / "version.json"
    assert version_path.exists()
    # check execution
    lsp_engine = LSPEngine.from_config_path(config_path)
    with TemporaryDirectory() as input_source:
        with TemporaryDirectory() as output_folder:
            transpile_config = TranspileConfig(
                transpiler_config_path=str(config_path),
                source_dialect="oracle",
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
            transpiled = format_transpiled(result.transpiled_code)
            assert transpiled == sql_code


async def test_installs_and_runs_local_morpheus(morpheus_artifact):
    await installer_lock.acquire()
    os.chdir(base_cwd)
    try:
        # TODO temporary workaround for RecursionError with temp dirs on Windows
        if sys.platform == "win32":
            await _install_and_run_pypi_bladerunner()
        else:
            with TemporaryDirectory() as tmpdir:
                with patch.object(TranspilerInstaller, "labs_path", return_value=Path(tmpdir)):
                    await _install_and_run_local_morpheus(morpheus_artifact)
    finally:
        installer_lock.release()


async def _install_and_run_local_morpheus(morpheus_artifact):
    # TODO: Test that running with existing install does nothing
    # TODO: Test that running with legacy install upgrades it
    # check new install
    morpheus = TranspilerInstaller.transpilers_path() / "morpheus"
    assert not morpheus.exists()
    # fresh install
    TranspilerInstaller.install_from_maven(
        "morpheus", "com.databricks.labs", "databricks-morph-plugin", morpheus_artifact
    )
    # check file-level installation
    morpheus = TranspilerInstaller.transpilers_path() / "morpheus"
    config_path = morpheus / "lib" / "config.yml"
    assert config_path.exists()
    main_path = morpheus / "lib" / "databricks-morph-plugin.jar"
    assert main_path.exists()
    version_path = morpheus / "state" / "version.json"
    assert version_path.exists()
    # check execution
    lsp_engine = LSPEngine.from_config_path(config_path)
    with TemporaryDirectory() as input_source:
        with TemporaryDirectory() as output_folder:
            transpile_config = TranspileConfig(
                transpiler_config_path=str(config_path),
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
            sql_code = "select * from employees;"
            result = await lsp_engine.transpile(dialect, "databricks", sql_code, input_file)
            await lsp_engine.shutdown()
            transpiled = format_transpiled(result.transpiled_code)
            assert transpiled == sql_code
