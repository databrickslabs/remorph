import logging
import yaml
import duckdb

from databricks.labs.remorph.assessments.profiler_config import PipelineConfig, Step
from databricks.labs.remorph.connections.database_manager import DatabaseManager

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class PipelineClass:
    def __init__(self, config: PipelineConfig, executor: DatabaseManager):
        self.config = config
        self.executor = executor

    def execute(self):
        logging.info(f"Pipeline initialized with config: {self.config.name}, version: {self.config.version}")
        for step in self.config.steps:
            if step.flag == "active":
                logging.debug(f"Executing step: {step.name}")
                self._execute_step(step)
        logging.info("Pipeline execution completed")

    def _execute_step(self, step: Step):
        logging.debug(f"Reading query from file: {step.extract_query}")
        with open(step.extract_query, 'r', encoding='utf-8') as file:
            query = file.read()

        # Execute the query using the database manager
        logging.debug(f"Executing query: {query}")
        result = self.executor.execute_query(query)

        # Save the result to SQLite
        self._save_to_db(result, step.name, str(step.mode))

    def _save_to_db(self, result, step_name: str, mode: str, batch_size: int = 1000):
        conn = duckdb.connect('pipeline_results.duckdb')
        columns = result.keys()
        schema = ', '.join(columns)

        # Handle write modes
        if mode == 'overwrite':
            conn.execute(f"CREATE OR REPLACE TABLE {step_name} ({schema})")
        elif mode == 'append' and step_name not in conn.get_table_names(""):
            conn.execute(f"CREATE TABLE {step_name} ({schema})")

        # Batch insert using prepared statements
        placeholders = ', '.join(['?' for _ in columns])
        insert_query = f"INSERT INTO {step_name} VALUES ({placeholders})"

        # Fetch and insert rows in batches
        while True:
            rows = result.fetchmany(batch_size)
            if not rows:
                break
            conn.executemany(insert_query, rows)

        conn.close()

    @staticmethod
    def load_config_from_yaml(file_path: str) -> PipelineConfig:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        steps = [Step(**step) for step in data['steps']]
        return PipelineConfig(name=data['name'], version=data['version'], steps=steps)
