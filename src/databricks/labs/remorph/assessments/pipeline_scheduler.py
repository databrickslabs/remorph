import time
import logging
from dataclasses import dataclass
from enum import Enum

from datetime import datetime, timezone
from databricks.labs.remorph.assessments.duckdb_manager import DuckDBManager
from databricks.labs.remorph.assessments.pipeline import PipelineClass, StepExecutionStatus
from databricks.labs.remorph.assessments.profiler_config import Step


def get_hours_since_last_run(last_run_datetime: datetime) -> int:
    """Returns the number of full hours that have elapsed since the given last run."""
    elapsed_time = datetime.now(timezone.utc) - last_run_datetime
    elapsed_seconds = elapsed_time.total_seconds()
    return round(elapsed_seconds // 3600)


def get_days_since_last_run(last_run_datetime: datetime) -> int:
    """Returns the number of full days that have elapsed since the given last run."""
    elapsed_time = datetime.now(timezone.utc) - last_run_datetime
    elapsed_seconds = elapsed_time.total_seconds()
    return round(elapsed_seconds // 86400)


class ScheduledFrequency(Enum):
    ONCE = "ONCE"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


@dataclass
class PollingStatus:
    polling_dt: datetime
    pipeline_name: str
    step_name: str
    status: str


class PipelineScheduler:
    """
    Executes a Pipeline's steps according to predefined Step schedules.
    """

    def __init__(self, pipelines: list[PipelineClass], polling_interval_secs: int = 5):

        self.duckdb_connection = DuckDBManager().get_connection()
        self.polling_interval = polling_interval_secs
        self.pipelines: list[PipelineClass] = pipelines

        # Create a table in DuckDB for maintaining pipeline state
        self._init_db()

    def _init_db(self):
        """Initializes a DuckDB database to store pipeline step execution state."""
        logging.info("Initializing pipeline state database...")
        self.duckdb_connection.execute(
            query="""
            CREATE TABLE IF NOT EXISTS pipeline_step_state (
                step_name TEXT,
                pipeline_name TEXT,
                last_run TIMESTAMPTZ,
                status TEXT,
                PRIMARY KEY (pipeline_name, step_name)
            )
        """
        )
        logging.info("DuckDB state table is initialized.")

    def _get_last_run_time(self, pipeline_name: str, step_name: str) -> tuple[datetime | None, str | None]:
        """Fetches the last execution time of a pipeline step from the database."""
        full_step_name = f"{pipeline_name}__{step_name}"
        last_run = None
        status = None
        result = self.duckdb_connection.execute(
            query="SELECT last_run, status FROM pipeline_step_state WHERE step_name = ?", parameters=[full_step_name]
        ).fetchone()
        if result is not None:
            last_run, status = result
        return last_run, status

    def _record_run_time(self, pipeline_name: str, step_name: str, status: str = StepExecutionStatus.COMPLETE.value):
        """Records the latest execution time of a pipeline step."""
        now = datetime.now(timezone.utc)
        full_step_name = f"{pipeline_name}__{step_name}"
        self.duckdb_connection.execute(
            query="""
            INSERT INTO pipeline_step_state (step_name, pipeline_name, last_run, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(pipeline_name, step_name)
                DO UPDATE SET
                last_run = EXCLUDED.last_run,
                status = EXCLUDED.status
        """,
            parameters=[full_step_name, pipeline_name, now, status],
        )

    def _should_run(self, pipeline_name: str, step: Step) -> bool:
        """Determines if a pipeline step should run based on its schedule."""
        scheduled_frequency = step.frequency
        last_run_time, status = self._get_last_run_time(pipeline_name, step.name)
        if last_run_time is None or status == StepExecutionStatus.ERROR.value:
            # First time running the Step
            should_run = True
            logging.info(f"First time running the step: '{step.name}'.")
        # The Step has been run once already
        elif scheduled_frequency == ScheduledFrequency.ONCE.value:
            logging.info(f"Step '{step.name}' has already been run once. Skipping.")
            should_run = False
        # Check if it's been >= 24 hours since the last run
        elif scheduled_frequency == ScheduledFrequency.DAILY.value and get_hours_since_last_run(last_run_time) >= 24:
            should_run = True
            logging.info(f"Running daily step '{step.name}' now.")
        # Check if it's been >= 7 days since the last run
        elif scheduled_frequency == ScheduledFrequency.WEEKLY.value and get_days_since_last_run(last_run_time) >= 7:
            should_run = True
            logging.info(f"Running weekly step '{step.name}' now.")
        else:
            # None of the triggering frequency conditions have been met
            should_run = False
        return should_run

    def _run_step(self, pipeline: PipelineClass, step: Step) -> str:
        """Executes a pipeline step if it's time to run."""
        if self._should_run(pipeline.config.name, step):
            status = str(pipeline.execute_step(step).value)
            self._record_run_time(pipeline.config.name, step.name, status)
        else:
            status = StepExecutionStatus.SKIPPED.value
        return status

    def run(self, num_polling_cycles: int = 1) -> list[PollingStatus]:
        """
        Loops over a pipeline's steps and checks if step has been executed
        according to its scheduled frequency.
        """
        logging.info("PipelineScheduler has started...")
        cycle_counter = 0
        polling_status = []
        while cycle_counter < num_polling_cycles:

            # Loop through the list of scheduled pipelines
            # TODO: Parallelize this in the future to be more efficient
            for pipeline in self.pipelines:
                pipeline_steps = pipeline.config.steps
                for pipeline_step in pipeline_steps:
                    # Inspect the execution frequency of the Step
                    # Possible frequencies include: "once", "daily", "weekly" (see `ScheduledFrequency` enum)
                    logging.info(f"Evaluating scheduling step '{pipeline_step.name}'.")
                    step_exec_status = self._run_step(pipeline, pipeline_step)
                    execution_status = PollingStatus(
                        datetime.now(timezone.utc), pipeline.config.name, pipeline_step.name, step_exec_status
                    )
                    polling_status.append(execution_status)

            # Wait a bit before polling status
            time.sleep(self.polling_interval)
            cycle_counter += 1

        return polling_status
