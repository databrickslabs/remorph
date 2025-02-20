from pathlib import Path
import duckdb
import pytest

from databricks.labs.remorph.assessments.pipeline import PipelineClass, DB_PATH
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
        step.extract_query = f"{prefix}/../../{step.extract_query}"
    return config


def test_run_pipeline(extractor, pipeline_config, get_logger):
    pipeline = PipelineClass(config=pipeline_config, executor=extractor)
    pipeline.execute()
    assert verify_output(get_logger)


def verify_output(get_logger):
    conn = duckdb.connect(DB_PATH)
    expected_tables = ["usage", "inventory"]
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
