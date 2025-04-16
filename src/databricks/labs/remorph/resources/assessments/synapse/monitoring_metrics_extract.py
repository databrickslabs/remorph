import duckdb
import argparse
import json
import sys
import logging
import urllib3
from .profiler_functions import get_synapse_workspace_settings, get_synapse_profiler_settings, get_synapse_artifacts_client, get_azure_metrics_query_client
from .profiler_classes import SynapseWorkspace, SynapseMetrics


def execute():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Generate and store random dataset in DuckDB')
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
        synapse_workspace_settings = get_synapse_workspace_settings()
        synapse_profiler_settings  = get_synapse_profiler_settings()
        workspace_tz = synapse_workspace_settings["tz_info"]

        workspace_name = synapse_workspace_settings["name"]
        logger.info(f"workspace_name → {workspace_name}")

        artifacts_client = get_synapse_artifacts_client()
        workspace_instance = SynapseWorkspace(workspace_tz, artifacts_client)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        metrics_client = get_azure_metrics_query_client()
        synapse_metrics = SynapseMetrics(metrics_client)

        workspace_info = workspace_instance.get_workspace_info()

        if not "id" in workspace_
            raise ValueError("ERROR: Missing Workspace ID for extracting Workspace Level Metrics")
        workspace_resource_id = workspace_info["id"]
        logger.info(f"workspace_resource_id  →  {workspace_resource_id}")
        metrics_df = synapse_metrics.get_workspace_level_metrics(workspace_resource_id)


        # SQL Pool Metrics

        exclude_dedicated_sql_pools = synapse_profiler_settings.get("exclude_dedicated_sql_pools", None)
        dedicated_sql_pools_profiling_list = synapse_profiler_settings.get("dedicated_sql_pools_profiling_list", None)

        logger.info(f" exclude_dedicated_sql_pools        →  {exclude_dedicated_sql_pools}")
        logger.info(f" dedicated_sql_pools_profiling_list →  {dedicated_sql_pools_profiling_list}")

        if exclude_dedicated_sql_pools  == True:
            logger.info(f" exclude_dedicated_sql_pools is set to {exclude_dedicated_sql_pools}, Skipping metrics extract for Dedicated SQL pools")
        else:
            dedicated_sqlpools = workspace_instance.list_sql_pools()
            all_dedicated_pools_list = [ pool for poolPages in dedicated_sqlpools for pool in poolPages]
            dedicated_pools_to_profile = all_dedicated_pools_list if not dedicated_sql_pools_profiling_list else [pool for pool in all_dedicated_pools_list if pool['name'] in dedicated_sql_pools_profiling_list]

            logger.info(f" Pool names to extract metrics: {[entry['name'] for entry in dedicated_pools_to_profile]}")

        if exclude_dedicated_sql_pools  == True:
            logger.info(f" exclude_dedicated_sql_pools is set to {exclude_dedicated_sql_pools}, Skipping metrics extract for Dedicated SQL pools")
        else:
            for idx, pool in enumerate(dedicated_pools_to_profile):
                pool_name = pool['name']
                pool_resoure_id = pool['id']

                logger.info(f"{'*'*70}")
                logger.info(f"{idx+1}) Pool Name: {pool_name}")
                logger.info(f"   Resource id: {pool_resoure_id}")

                step_name = "dedicated_sql_pool_metrics"
                metrics_staging_uxpath = get_staging_linux_path(extract_group_name, True)

                step_extractor = ProfilerStepPartitionExtractor(step_name, metrics_staging_uxpath, "pool_name", pool_name)
                step_extractor.extract(lambda: synapse_metrics.get_dedicated_sql_pool_metrics(pool_resoure_id),  workspace_name)
            logger.info(">End")

        # MAGIC ### 2. Spark Pool  Metrics
        # MAGIC > Extract Metrics for Spark Pools

        # COMMAND ----------

        exclude_spark_pools = synapse_profiler_settings.get("exclude_spark_pools", None)
        spark_pools_profiling_list = synapse_profiler_settings.get("spark_pools_profiling_list", None)

        logger.info(f" exclude_spark_pools        →  {exclude_spark_pools}")
        logger.info(f" spark_pools_profiling_list →  {spark_pools_profiling_list}")

        # COMMAND ----------

        # DBTITLE 1,Get List of Pools to extract Metrics
        if exclude_spark_pools  == True:
            logger.info(f" exclude_spark_pools is set to {exclude_spark_pools}, Skipping metrics extract for Spark pools")
        else:
            spark_pools_iter = workspace_instance.list_bigdata_pools()
            all_spark_pool_list = [ pool for poolPages in spark_pools_iter for pool in poolPages]
            spark_pools_to_profile = all_spark_pool_list if not spark_pools_profiling_list else [pool for pool in all_spark_pool_list if pool['name'] in spark_pools_profiling_list]

            logger.info(f" Pool names to extract metrics: {[entry['name'] for entry in spark_pools_to_profile]}")

        # COMMAND ----------

        # DBTITLE 1,Run Metrics Extract for Each Pool
        if exclude_spark_pools  == True:
            logger.info(f" exclude_spark_pools is set to {exclude_spark_pools}, Skipping metrics extract for Spark pools")
        else:
            for idx, pool in enumerate(spark_pools_to_profile):
                pool_name = pool['name']
                pool_resoure_id = pool['id']

                logger.info(f"{'*'*70}")
                logger.info(f"{idx+1}) Pool Name: {pool_name}")
                logger.info(f"   Resource id: {pool_resoure_id}")

                step_name = "spark_pool_metrics"
                metrics_staging_uxpath = get_staging_linux_path(extract_group_name, True)

                step_extractor = ProfilerStepPartitionExtractor(step_name, metrics_staging_uxpath, "pool_name", pool_name)
                step_extractor.extract(lambda: synapse_metrics.get_spark_pool_metrics(pool_resoure_id),  workspace_name)
            logger.info(">End")

        # Connect to DuckDB
        conn = duckdb.connect(args.db_path)

        # Create table with appropriate schema
        conn.execute(
            """
            CREATE OR REPLACE TABLE random_data (
                id INTEGER,
                date TIMESTAMP,
                category VARCHAR,
                department VARCHAR,
                is_active BOOLEAN,
                score DOUBLE
            )
        """
        )

        conn.execute("INSERT INTO random_data SELECT * FROM df")
        conn.close()
        # This is the output format expected by the pipeline.py which orchestrates the execution of this script
        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    execute()
