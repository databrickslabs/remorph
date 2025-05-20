python
import json
import sys
import logging
from databricks.labs.remorph.resources.assessments.synapse.common.functions import (
    arguments_loader,
    get_config,
    get_synapse_artifacts_client
)
import zoneinfo
from databricks.labs.remorph.resources.assessments.synapse.common.profiler_classes import SynapseWorkspace

def execute():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    db_path, creds_file = arguments_loader(description="Synapse Synapse Serverless SQL Pool Extract Script")

    try:
        synapse_workspace_settings = get_config(creds_file)["synapse"]
        synapse_profiler_settings = synapse_workspace_settings["profiler"]

        tz_info = synapse_workspace_settings["workspace"]["tz_info"]
        workspace_tz = zoneinfo.ZoneInfo(tz_info)
        artifacts_client = get_synapse_artifacts_client(synapse_workspace_settings)
        workspace = SynapseWorkspace(workspace_tz, artifacts_client)

        if not synapse_profiler_settings.get("exclude_serverless_sql_pool", False):
            try:
                # Ensure dbutils is available in your environment
                databases_profiled = dbutils.notebook.run("./04_serverless_sqlpool_info_extract", 0)
                print(f'INFO: Successfully extracted information for databases {databases_profiled}')
                dbutils.notebook.run("./04_serverless_sqlpool_activity_extract", 0)
            except NameError:
                logger.error("dbutils is not available. This script must be run in a Databricks environment.")
                print(json.dumps({"status": "error", "message": "dbutils not available"}), file=sys.stderr)
                sys.exit(1)
        else:
            print('INFO: "exclude_serverless_sql_pool" configuration is set to True. Skipping Serverless Pool extracts.')

        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    execute()
