import duckdb
import argparse
import json
import sys
import logging
import urllib3
import pandas as pd
from .profiler_functions import (
    get_synapse_workspace_settings,
    get_synapse_profiler_settings,
    get_synapse_artifacts_client,
    get_azure_metrics_query_client,
)
from .profiler_classes import SynapseWorkspace, SynapseMetrics


def execute():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Extract Synapse workspace artifacts and store in DuckDB')
    parser.add_argument('--db-path', type=str, required=True, help='Path to DuckDB database file')
    parser.add_argument(
        '--credential-config-path', type=str, required=True, help='Path string containing credential configuration'
    )
    args = parser.parse_args()
    credential_file = args.credential_config_path

    if not credential_file.endswith('credentials.yml'):
        msg = "Credential config file must have 'credentials.yml' extension"
        # This is the output format expected by the pipeline.py which orchestrates the execution of this script
        print(json.dumps({"status": "error", "message": msg}), file=sys.stderr)
        raise ValueError("Credential config file must have 'credentials.yml' extension")

    try:
        # Initialize workspace settings and client
        synapse_workspace_settings = get_synapse_workspace_settings()
        synapse_profiler_settings = get_synapse_profiler_settings()
        workspace_tz = synapse_workspace_settings["tz_info"]
        workspace_name = synapse_workspace_settings["name"]
        logger.info(f"workspace_name → {workspace_name}")

        artifacts_client = get_synapse_artifacts_client()
        workspace = SynapseWorkspace(workspace_tz, artifacts_client)

        # Extract workspace info
        workspace_info = workspace.get_workspace_info()
        workspace_info_df = pd.DataFrame([workspace_info])
        insert_df_to_duckdb(workspace_info_df, args.db_path, "workspace_info")

        # Extract SQL pools
        sql_pools = workspace.list_sql_pools()
        sql_pools_df = pd.DataFrame([pool for pool_pages in sql_pools for pool in pool_pages])
        insert_df_to_duckdb(sql_pools_df, args.db_path, "sql_pools")

        # Extract Spark pools
        spark_pools = workspace.list_bigdata_pools()
        spark_pools_df = pd.DataFrame([pool for pool_pages in spark_pools for pool in pool_pages])
        insert_df_to_duckdb(spark_pools_df, args.db_path, "spark_pools")

        # Extract Linked Services
        linked_services = workspace.list_linked_services()
        linked_services_df = pd.DataFrame(linked_services)
        insert_df_to_duckdb(linked_services_df, args.db_path, "linked_services")

        # Extract Data Flows
        dataflows = workspace.list_data_flows()
        dataflows_df = pd.DataFrame(dataflows)
        insert_df_to_duckdb(dataflows_df, args.db_path, "dataflows")

        # Extract Pipelines
        pipelines = workspace.list_pipelines()
        pipelines_df = pd.DataFrame(pipelines)
        insert_df_to_duckdb(pipelines_df, args.db_path, "pipelines")

        # Extract Spark Jobs
        spark_jobs = workspace.list_spark_job_definitions()
        spark_jobs_df = pd.DataFrame(spark_jobs)
        insert_df_to_duckdb(spark_jobs_df, args.db_path, "spark_jobs")

        # Extract Notebooks
        notebooks = workspace.list_notebooks()
        notebooks_df = pd.DataFrame(notebooks)
        insert_df_to_duckdb(notebooks_df, args.db_path, "notebooks")

        # Extract SQL Scripts
        sql_scripts = workspace.list_sqlscripts()
        sql_scripts_df = pd.DataFrame(sql_scripts)
        insert_df_to_duckdb(sql_scripts_df, args.db_path, "sql_scripts")

        # Extract Triggers
        triggers = workspace.list_triggers()
        triggers_df = pd.DataFrame(triggers)
        insert_df_to_duckdb(triggers_df, args.db_path, "triggers")

        # Extract Libraries
        libraries = workspace.list_libraries()
        libraries_df = pd.DataFrame(libraries)
        insert_df_to_duckdb(libraries_df, args.db_path, "libraries")

        # Extract Datasets
        datasets = workspace.list_datasets()
        datasets_df = pd.DataFrame(datasets)
        insert_df_to_duckdb(datasets_df, args.db_path, "datasets")

        # Extract Pipeline Runs (last 60 days)
        from datetime import date, timedelta
        today = date.today()
        pipeline_runs_list = []
        for days in range(1, 60):
            last_upd = today + timedelta(days=-days)
            pipeline_runs = workspace.list_pipeline_runs(last_upd)
            for run in pipeline_runs:
                run['last_upd'] = last_upd
                pipeline_runs_list.append(run)
        pipeline_runs_df = pd.DataFrame(pipeline_runs_list)
        insert_df_to_duckdb(pipeline_runs_df, args.db_path, "pipeline_runs")

        # Extract Trigger Runs (last 60 days)
        trigger_runs_list = []
        for days in range(1, 60):
            last_upd = today + timedelta(days=-days)
            trigger_runs = workspace.list_trigger_runs(last_upd)
            for run in trigger_runs:
                run['last_upd'] = last_upd
                trigger_runs_list.append(run)
        trigger_runs_df = pd.DataFrame(trigger_runs_list)
        insert_df_to_duckdb(trigger_runs_df, args.db_path, "trigger_runs")

        # This is the output format expected by the pipeline.py which orchestrates the execution of this script
        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)


def insert_df_to_duckdb(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    """
    Insert a pandas DataFrame into a DuckDB table.
    
    Args:
        df (pd.DataFrame): The pandas DataFrame to insert
        db_path (str): Path to the DuckDB database file
        table_name (str): Name of the table to insert data into
    """
    try:
        # Connect to DuckDB
        conn = duckdb.connect(db_path)
        
        # Create table if it doesn't exist
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df LIMIT 0")
        
        # Insert data
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        
        # Close connection
        conn.close()
        logging.info(f"Successfully inserted data into {table_name} table")
    except Exception as e:
        logging.error(f"Error inserting data into DuckDB: {str(e)}")
        raise


if __name__ == '__main__':
    execute()

