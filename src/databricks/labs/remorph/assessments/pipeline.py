import logging
import yaml
import duckdb
import pandas as pd

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

    def _save_to_db(self, result, step_name: str, mode: str):
        conn = duckdb.connect('pipeline_results.duckdb')
        cursor = conn.cursor()
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        print(df.head(5))


        # Save result to Parquet file
        if mode == "overwrite":
            logging.debug(f"Overwriting table: {step_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {step_name}")
            cursor.execute(f"CREATE TABLE {step_name} AS SELECT * FROM {df}")
        elif mode == "append":
            logging.debug(f"Appending to table: {step_name}")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {step_name} AS {df} LIMIT 0")
            cursor.execute(f"INSERT INTO {step_name} SELECT * FROM {df}")

        conn.close()

    @staticmethod
    def load_config_from_yaml(file_path: str) -> PipelineConfig:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        steps = [Step(**step) for step in data['steps']]
        return PipelineConfig(name=data['name'], version=data['version'], steps=steps)
