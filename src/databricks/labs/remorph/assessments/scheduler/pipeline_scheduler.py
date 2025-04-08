import time
import logging
import duckdb
from datetime import datetime

from databricks.labs.remorph.assessments.pipeline import PipelineClass
from databricks.labs.remorph.assessments.profiler_config import Step


def _get_hours_since_last_run(last_run_datetime: datetime) -> int:
    elapsed_time = datetime.now() - last_run_datetime
    elapsed_seconds = elapsed_time.total_seconds()
    return int(divmod(elapsed_seconds, 3600)[0])


def _get_days_since_last_run(last_run_datetime: datetime) -> int:
    elapsed_time = datetime.now() - last_run_datetime
    elapsed_seconds = elapsed_time.total_seconds()
    return int(divmod(elapsed_seconds, 86400)[0])


class PipelineScheduler:
    """A scheduler that executes Pipeline steps according to predefined schedules."""

    def __init__(self, pipelines: list[PipelineClass],
                 db_path: str = "pipeline_steps.duckdb",
                 polling_interval_secs: int = 5):

        self.db_path = db_path
        self.polling_interval = polling_interval_secs
        self.pipelines: list[PipelineClass] = pipelines

        # Create a table in DuckDB for maintaining pipeline state
        self._init_db()

    def _init_db(self):
        """Initializes a DuckDB database to store pipeline step execution state."""
        logging.info("Initializing pipeline state database...")
        with duckdb.connect(self.db_path) as conn:
            conn.execute(query="""
                CREATE OR REPLACE TABLE pipeline_step_state (
                    step_name TEXT PRIMARY KEY,
                    pipeline_name TEXT,
                    last_run TIMESTAMP,
                    status TEXT
                )
            """)
        logging.info("DuckDB state table is ready to go!")

    def _get_last_run_time(self, pipeline_name: str, step_name: str) -> datetime | None:
        """Fetches the last execution time of a pipeline step from the database. """
        with duckdb.connect(self.db_path) as conn:
            full_step_name = f"{pipeline_name}__{step_name}"
            result = conn.execute(query="SELECT last_run FROM pipeline_step_state WHERE step_name = ?",
                                  parameters=[full_step_name]).fetchone()
            if result is not None:
                last_run_time_str = result[0]
                return last_run_time_str
            else:
                return None

    def _record_run_time(self, pipeline_name: str, step_name: str, status: str = "COMPLETE"):
        """Records the latest execution time of a pipeline step."""
        with duckdb.connect(self.db_path) as conn:
            now = datetime.now()
            full_step_name = f"{pipeline_name}__{step_name}"
            conn.execute(query="""
                INSERT INTO pipeline_step_state (step_name, pipeline_name, last_run, status)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(step_name)
                  DO UPDATE
                  SET pipeline_name = excluded.pipeline_name, last_run = excluded.last_run, status = excluded.status
            """, parameters=[full_step_name, pipeline_name, now, status])

    def _should_run(self, pipeline_name: str, step: Step) -> bool:
        """Determines if a pipeline step should run based on its schedule."""
        scheduled_frequency = step.frequency
        last_run_time = self._get_last_run_time(pipeline_name, step.name)
        if last_run_time is None:
            # First time running the Step
            should_run = True
            logging.info(f"First time running the step: '{step.name}'.")
        else:
            # The Step has been run once already
            if scheduled_frequency == "once":
                logging.info(f"Step '{step.name}' has already been run once. Skipping.")
                should_run = False
            # Check if it's been >= 24 hours since the last run
            elif scheduled_frequency == "daily" and _get_hours_since_last_run(last_run_time) >= 24:
                should_run = True
                logging.info(f"Running daily step '{step.name}' now.")
            # Check if it's been >= 7 days since the last run
            elif scheduled_frequency == "weekly" and _get_days_since_last_run(last_run_time) >= 7:
                should_run = True
                logging.info(f"Running weekly step '{step.name}' now.")
            else:
                # None of the triggering frequency conditions have been met
                should_run = False
        return should_run

    def _run_step(self, pipeline: PipelineClass, step: Step):
        """Executes a pipeline step if it's time to run."""
        if self._should_run(pipeline.config.name, step):
            status = pipeline.execute_step(step)
            self._record_run_time(pipeline.config.name, step.name, status)

    def run(self, num_cycles: int = None):
        """Create an infinite loop over the pipeline steps"""
        logging.info("PipelineScheduler has started...")
        cycle_counter = 0
        while cycle_counter < num_cycles if num_cycles is not None else True:

            # Loop through the list of scheduled pipelines
            # TODO: Parallelize this in the future to be more efficient
            for pipeline in self.pipelines:
                pipeline_steps = pipeline.config.steps
                for pipeline_step in pipeline_steps:
                    # Inspect the execution frequency of the Step
                    # Possible frequencies include: "once", "daily", "weekly"
                    logging.info(f"Evaluating scheduling step '{pipeline_step.name}'.")
                    self._run_step(pipeline, pipeline_step)

            # Wait a bit before polling status
            time.sleep(self.polling_interval)
            if num_cycles is not None:
                cycle_counter += 1
