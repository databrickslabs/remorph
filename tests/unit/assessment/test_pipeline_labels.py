from pathlib import Path

import pytest

from databricks.labs.lakebridge.assessments.pipeline import PipelineClass, StepExecutionStatus
from databricks.labs.lakebridge.assessments.profiler_config import PipelineConfig, Step, StepLabel


@pytest.mark.parametrize(
    ("skip_labels", "expected_status"),
    (
        # Label skipped: skipped before the step needs a connector.
        (frozenset({StepLabel.UNREDACTED}), StepExecutionStatus.SKIPPED),
        # Label not skipped: the step runs, and fails here because there is no connector.
        (frozenset(), StepExecutionStatus.ERROR),
    ),
)
def test_skip_labels(tmp_path: Path, skip_labels: frozenset[StepLabel], expected_status: StepExecutionStatus) -> None:
    query = tmp_path / "query.sql"
    query.write_text("SELECT 1", encoding="utf-8")
    step = Step(name="labelled_step", type="sql", extract_source=str(query), label=StepLabel.UNREDACTED)
    config = PipelineConfig(name="test", version="1.0", steps=[step])

    pipeline = PipelineClass(
        config,
        executor=None,
        db_path=tmp_path / "extract.db",
        cred_file_path=tmp_path / "creds.yml",
        skip_labels=skip_labels,
    )
    results = pipeline.execute()

    assert [r.status for r in results] == [expected_status]
