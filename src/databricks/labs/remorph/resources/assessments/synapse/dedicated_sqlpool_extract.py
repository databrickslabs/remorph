import json
import sys
import logging
from databricks.labs.remorph.resources.assessments.synapse.common.functions import (
    arguments_loader,
    get_config,
    get_synapse_artifacts_client,
)
import zoneinfo
from databricks.labs.remorph.resources.assessments.synapse.common.profiler_classes import SynapseWorkspace

def execute():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    db_path, creds_file = arguments_loader(description="Synapse Synapse Dedicated SQL Pool Extract Script")

    try:
        synapse_workspace_settings = get_config(creds_file)["synapse"]
        synapse_profiler_settings = synapse_workspace_settings["profiler"]

        tz_info = synapse_workspace_settings["workspace"]["tz_info"]
        workspace_tz = zoneinfo.ZoneInfo(tz_info)
        exclude_dedicated_sql_pools = synapse_profiler_settings.get("exclude_dedicated_sql_pools", None)
        dedicated_sql_pools_profiling_list = synapse_profiler_settings.get("dedicated_sql_pools_profiling_list", None)
        artifacts_client = get_synapse_artifacts_client(synapse_workspace_settings)
        workspace = SynapseWorkspace(workspace_tz, artifacts_client)

        if exclude_dedicated_sql_pools:
            logger.info(f"exclude_dedicated_sql_pools is set to {exclude_dedicated_sql_pools}, Skipping metrics extract for Dedicated SQL pools")
            print(json.dumps({"status": "success", "message": "Data loaded successfully"}))
            return

        dedicated_sqlpools = workspace.list_sql_pools()
        all_dedicated_pools_list = [pool for poolPages in dedicated_sqlpools for pool in poolPages]
        if dedicated_sql_pools_profiling_list:
            dedicated_pools_to_profile = [pool for pool in all_dedicated_pools_list if pool['name'] in dedicated_sql_pools_profiling_list]
        else:
            dedicated_pools_to_profile = all_dedicated_pools_list

        logger.info("Pool names to extract metrics...")
        for idx, entry in enumerate(dedicated_pools_to_profile):
            print(f"\t {idx+1}  {entry['name'].ljust(50, '.')}{entry['status']}")

        live_dedicated_pools_to_profile = [entry for entry in dedicated_pools_to_profile if entry['status'] == 'Online']
        logger.info(f"live_dedicated_pools_to_profile: {[entry['name'] for entry in live_dedicated_pools_to_profile]}")

        # Info: Extract
        for idx, entry in enumerate(live_dedicated_pools_to_profile):
            entry_info = f"{entry['name']} [{entry['status']}]"
            print(f"   {idx:02d})  {entry_info.ljust(60, '.')} : RUNNING extract...")
            logger.info("./04_dedicated_sqlpool_info_extract")

        # Activity: Extract
        sqlpool_names_to_profile = ",".join([entry['name'] for entry in live_dedicated_pools_to_profile])
        logger.info(f"Running 04_dedicated_sqlpools_activity_extract with sqlpool_names  → [{sqlpool_names_to_profile}] ...")
        logger.info("./04_dedicated_sqlpools_activity_extract", 0, {"sqlpool_names": sqlpool_names_to_profile})

        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    execute()
