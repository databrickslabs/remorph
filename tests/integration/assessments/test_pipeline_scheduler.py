from pathlib import Path
import pytest

from databricks.labs.remorph.assessments.pipeline import PipelineClass
from databricks.labs.remorph.assessments.scheduler.pipeline_scheduler import PipelineScheduler
from ..connections.helpers import get_db_manager


@pytest.fixture()
def extractor():
    return get_db_manager("remorph", "postgres")


@pytest.fixture(scope="module")
def pipeline_config():
    prefix = Path(__file__).parent
    config_path = f"{prefix}/../../resources/assessments/scheduler/postgres_pipeline_config.yml"
    config = PipelineClass.load_config_from_yaml(config_path)

    for step in config.steps:
        step.extract_source = f"{prefix}/../../{step.extract_source}"
    return config


def test_pipeline_scheduler(pipeline_config, extractor):
    simple_pipeline = PipelineClass(config=pipeline_config, executor=extractor)
    pipelines = [simple_pipeline]
    scheduler = PipelineScheduler(pipelines)
    scheduler.run(num_cycles=3)
    assert 1 == 1
