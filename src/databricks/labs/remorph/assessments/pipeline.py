from pathlib import Path

import json
import logging
import subprocess
import yaml
import duckdb

from databricks.labs.remorph.connections.credential_manager import cred_file

from databricks.labs.remorph.assessments.profiler_config import PipelineConfig, Step
from databricks.labs.remorph.connections.database_manager import DatabaseManager

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

DB_NAME = "profiler_extract.db"


class PipelineClass:
    def __init__(self, config: PipelineConfig, executor: DatabaseManager):
        self.config = config
        self.executor = executor
        self.db_path_prefix = Path(config.extract_folder)

    def execute(self):
        logging.info(f"Pipeline initialized with config: {self.config.name}, version: {self.config.version}")
        for step in self.config.steps:
            if step.flag == "active":
                logging.debug(f"Executing step: {step.name}")
                self._execute_step(step)
        logging.info("Pipeline execution completed")

    def _execute_step(self, step: Step):
        if step.type == "sql":
            self._execute_sql_step(step)
        elif step.type == "python":
            self._execute_python_step(step)
        else:
            logging.error(f"Unsupported step type: {step.type}")

    def _execute_sql_step(self, step: Step):
        logging.debug(f"Reading query from file: {step.extract_source}")
        with open(step.extract_source, 'r', encoding='utf-8') as file:
            query = file.read()

        # Execute the query using the database manager
        logging.info(f"Executing query: {query}")
        try:
            result = self.executor.execute_query(query)

            # Save the result to duckdb
            self._save_to_db(result, step.name, str(step.mode))
        except Exception as e:
            logging.error(f"SQL execution failed: {str(e)}")
            raise RuntimeError(f"SQL execution failed: {str(e)}") from e

    def _execute_python_step(self, step: Step):
        logging.debug(f"Executing Python script: {step.extract_source}")
        db_path = str(self.db_path_prefix / DB_NAME)
        credential_config = str(cred_file("remorph"))

        try:
            result = subprocess.run(
                ["python", step.extract_source, "--db-path", db_path, "--credential-config-path", credential_config],
                check=True,
                capture_output=True,
                text=True,
            )

            try:
                output = json.loads(result.stdout)
                if output["status"] == "success":
                    logging.info(f"Python script completed: {output['message']}")
                else:
                    raise RuntimeError(f"Script reported error: {output['message']}")
            except json.JSONDecodeError:
                logging.info(f"Python script output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr
            logging.error(f"Python script failed: {error_msg}")
            raise RuntimeError(f"Script execution failed: {error_msg}") from e

    def _execute_python_step(self, step: Step):
        logging.debug(f"Executing Python script: {step.extract_source}")
        db_path = str(self.db_path_prefix / DB_NAME)
        credential_config = str(cred_file("remorph"))

        try:
            result = subprocess.run(
                ["python", step.extract_source, "--db-path", db_path, "--credential-config-path", credential_config],
                check=True,
                capture_output=True,
                text=True,
            )

            try:
                output = json.loads(result.stdout)
                if output["status"] == "success":
                    logging.info(f"Python script completed: {output['message']}")
                else:
                    raise RuntimeError(f"Script reported error: {output['message']}")
            except json.JSONDecodeError:
                logging.info(f"Python script output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr
            logging.error(f"Python script failed: {error_msg}")
            raise RuntimeError(f"Script execution failed: {error_msg}") from e

    def _save_to_db(self, result, step_name: str, mode: str, batch_size: int = 1000):
        self._create_dir(self.db_path_prefix)
        conn = duckdb.connect(str(self.db_path_prefix) + '/' + DB_NAME)
        columns = result.keys()
        # TODO: Add support for figuring out data types from SQLALCHEMY result object result.cursor.description is not reliable
        schema = ' STRING, '.join(columns) + ' STRING'

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
    def _create_dir(dir_path: Path):
        if not Path(dir_path).exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_config_from_yaml(file_path: str) -> PipelineConfig:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        steps = [Step(**step) for step in data['steps']]
        return PipelineConfig(
            name=data['name'], version=data['version'], extract_folder=data['extract_folder'], steps=steps
        )
