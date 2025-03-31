from pathlib import Path
import pytest

from databricks.labs.remorph.assessments.pipeline import PipelineClass
from databricks.labs.remorph.assessments.scheduler.usage_collector import UsageCollector
from ..connections.helpers import get_db_manager


@pytest.fixture()
def extractor(mock_credentials):
    return get_db_manager("remorph", "postgres")


@pytest.fixture(scope="module")
def pipeline_config():
    prefix = Path(__file__).parent
    config_path = f"{prefix}/../../resources/assessments/scheduler/postgres_pipeline_config.yml"
    config = PipelineClass.load_config_from_yaml(config_path)

    for step in config.steps:
        step.extract_source = f"{prefix}/../../{step.extract_source}"
    return config


def test_usage_collector(pipeline_config, extractor):
    pg_pipeline = PipelineClass(config=pipeline_config, executor=extractor)
    usage_collector = UsageCollector(warehouse_type="Postgres", pipeline=pg_pipeline)
    status = usage_collector.run()
    assert status == "COMPLETE", "Usage collector returned an unexpected status."
