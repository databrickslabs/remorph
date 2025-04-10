from pathlib import Path
import duckdb
import pytest

from databricks.labs.remorph.assessments.pipeline import PipelineClass, DB_NAME
from ..connections.helpers import get_db_manager


@pytest.fixture()
def extractor(mock_credentials):
    return get_db_manager("remorph", "mssql")


@pytest.fixture(scope="module")
def pipeline_config():
    prefix = Path(__file__).parent
    config_path = f"{prefix}/../../resources/assessments/pipeline_config.yml"
    config = PipelineClass.load_config_from_yaml(config_path)

    for step in config.steps:
        step.extract_source = f"{prefix}/../../{step.extract_source}"
    return config

@pytest.fixture(scope="module")
def pipeline_dep_config():
    prefix = Path(__file__).parent
    config_path = f"{prefix}/../../resources/assessments/pipeline_config_dependency.yml"
    config = PipelineClass.load_config_from_yaml(config_path)

    for step in config.steps:
        step.extract_source = f"{prefix}/../../{step.extract_source}"
    return config

@pytest.fixture(scope="module")
def sql_failure_config():
    prefix = Path(__file__).parent
    config_path = f"{prefix}/../../resources/assessments/pipeline_config_sql_failure.yml"
    config = PipelineClass.load_config_from_yaml(config_path)
    for step in config.steps:
        step.extract_source = f"{prefix}/../../{step.extract_source}"
    return config


@pytest.fixture(scope="module")
def python_failure_config():
    prefix = Path(__file__).parent
    config_path = f"{prefix}/../../resources/assessments/pipeline_config_python_failure.yml"
    config = PipelineClass.load_config_from_yaml(config_path)
    for step in config.steps:
        step.extract_source = f"{prefix}/../../{step.extract_source}"
    return config


def test_run_pipeline(extractor, pipeline_config, get_logger):
    pipeline = PipelineClass(config=pipeline_config, executor=extractor)
    pipeline.execute()
    assert verify_output(get_logger, pipeline_config.extract_folder)


def test_run_sql_failure_pipeline(extractor, sql_failure_config, get_logger):
    pipeline = PipelineClass(config=sql_failure_config, executor=extractor)
    with pytest.raises(RuntimeError, match="SQL execution failed"):
        pipeline.execute()


def test_run_python_failure_pipeline(extractor, python_failure_config, get_logger):
    pipeline = PipelineClass(config=python_failure_config, executor=extractor)
    with pytest.raises(RuntimeError, match="Script execution failed"):
        pipeline.execute()

def test_run_python_dep_pipeline(extractor, pipeline_dep_config, get_logger):
    pipeline = PipelineClass(config=pipeline_dep_config, executor=extractor)
    pipeline.execute()
    assert verify_output(get_logger, pipeline_config.extract_folder)


def verify_output(get_logger, path):
    conn = duckdb.connect(str(Path(path)) + "/" + DB_NAME)

    expected_tables = ["usage", "inventory", "random_data"]
    logger = get_logger
    for table in expected_tables:
        try:
            result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            logger.info(f"Count for {table}: {result[0]}")
            if result[0] == 0:
                logger.debug(f"Table {table} is empty")
                return False
        except duckdb.CatalogException:
            logger.debug(f"Table {table} does not exist")
            return False

    conn.close()
    logger.info("All expected tables exist and are not empty")
    return True
