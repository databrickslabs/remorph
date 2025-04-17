from pathlib import Path
import pytest

from datetime import datetime

from databricks.labs.remorph.assessments.pipeline import PipelineClass
from databricks.labs.remorph.assessments.scheduler.pipeline_scheduler import PipelineScheduler, \
    get_hours_since_last_run, get_days_since_last_run
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


def test_hours_since_last_run():
    date_start_str = "2025-04-08 10:30:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    datetime_start = datetime.strptime(date_start_str, date_format)
    actual_hours = get_hours_since_last_run(datetime_start)
    expected_hours = divmod((datetime.now() - datetime_start).total_seconds(),  3600)[0]
    assert actual_hours == expected_hours, "The calculated hours since last run does not match the expected value."


def test_days_since_last_run():
    date_start_str = "2025-04-08 10:30:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    datetime_start = datetime.strptime(date_start_str, date_format)
    actual_days = get_days_since_last_run(datetime_start)
    expected_days = divmod((datetime.now() - datetime_start).total_seconds(),  86400)[0]
    assert actual_days == expected_days, "The calculated days since last run does not match the expected value."


def test_pipeline_scheduler(pipeline_config, extractor):
    simple_pipeline = PipelineClass(config=pipeline_config, executor=extractor)
    pipelines = [simple_pipeline]
    scheduler = PipelineScheduler(pipelines)
    status = scheduler.run(max_num_cycles=3)
    assert len(status) == 3, "The actual step execution statuses did not match the expected amount."
