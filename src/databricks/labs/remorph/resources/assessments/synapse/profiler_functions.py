
def get_synapse_workspace_settings():
    """
      Returns Synapse Workspace Settings
    """
    return synapse_workspace

def get_synapse_profiler_settings():
    """
      Returns Synapse Profiler Settings
    """
    return synapse_profiler

def get_synapse_jdbc_settings():
    """
      Returns Synapse JDBC settings
    """
    return synapse_jdbc

def get_sqlpool_reader(sql_endpoint, user, password):
    '''
      returns a jdbc reader for the given dedicated SQL Pool database
    '''
    return (spark.read
            .format("jdbc")
            .option("url", sql_endpoint)
            .option("user", user)
            .option("password", password)
            )



# DBTITLE 1,get_dedicated_sqlpool_reader
def get_dedicated_sqlpool_reader(db_name):
    '''
      returns a jdbc reader for the given dedicated SQL Pool database
    '''
    sql_endpoint = synapse_jdbc["dedicated_sqlpool_url_template"].format(endpoint=synapse_workspace["dedicated_sql_endpoint"], database=db_name)
    user = synapse_workspace["sql-user"]
    password = synapse_workspace["sql-password"]
    return get_sqlpool_reader(sql_endpoint, user, password);



# DBTITLE 1,get_serverless_sqlpool_reader
def get_serverless_sqlpool_reader():
    '''
      returns a jdbc reader for the given serverless SQL Pool database
    '''
    sql_endpoint = synapse_jdbc["serverless_sqlpool_url_template"].format(endpoint=synapse_workspace["serverless_sql_endpoint"])
    user = synapse_workspace["sql-user"]
    password = synapse_workspace["sql-password"]
    return get_sqlpool_reader(sql_endpoint, user, password);



# DBTITLE 1,get_staging_dbfs_path
import os
def get_staging_dbfs_path(group_name, create_if_not_exists = False):
    synapse_workspace_settings = get_synapse_workspace_settings()
    profiler_settings = get_synapse_profiler_settings()
    # Synaspse Workspce Name
    synapse_workspace_name = synapse_workspace_settings["name"]
    # data_staging_root
    data_staging_root =  profiler_settings["data_staging_root"]
    # Note: user sets data_staging_root as dbfs path
    #      to that we are going to add to following subfolder structure
    #     data_staging_root/{synapse_workspace_name}/{group_name}
    staging_dbfs_path = os.path.join(data_staging_root, synapse_workspace_name, group_name)
    print(f"INFO: get_staging_dbfs_path('{group_name}', {create_if_not_exists}) → {staging_dbfs_path}")
    # Create the dbfs path if required
    if create_if_not_exists:
        dbutils.fs.mkdirs(staging_dbfs_path)
    ignore = dbutils.fs.ls(data_staging_root) # test
    return staging_dbfs_path



# DBTITLE 1,dbfs_to_linux_path
import re
def dbfs_to_linux_path(dbfs_path):
    return re.sub(
        "^dbfs:",
        "",
        re.sub(
            "^(?!((dbfs:/Volumes)|(/Volumes)))((dbfs:)?)",
            "/dbfs",
            dbfs_path
        )
    );



# DBTITLE 1,get_staging_linux_path
import os, re
def get_staging_linux_path(group_name, create_if_not_exists = False):
    dbfs_path = get_staging_dbfs_path(group_name, create_if_not_exists)
    linux_path = dbfs_to_linux_path(dbfs_path)
    print(f"INFO: get_staging_linux_path('{group_name}', {create_if_not_exists}) → {linux_path}")
    return linux_path



# MAGIC %md
# MAGIC ##### > Azure SDK (Synapse) Utility Functions



# DBTITLE 1,get_synapse_artifacts_client
def get_synapse_artifacts_client():
    '''
        returns an Azure SDK client handle for Synapse Artifacts
    '''
    return ArtifactsClient (
        endpoint = synapse_workspace["development_endpoint"],
        credential = DefaultAzureCredential()
    )



# DBTITLE 1,get_azure_metrics_query_client
def get_azure_metrics_query_client():
    '''
        returns an Azure SDK Monitoring Mertics Client handle
    '''
    return MetricsQueryClient (DefaultAzureCredential())



# MAGIC %md
# MAGIC ##### > Misc Utility Functions



# DBTITLE 1,check_target_folder_content
# check_target_folder_content
def check_target_folder_content(target_Path, case_sensitive_schema = True, file_format="json"):
    # update session settings of required
    session_sql_case_sensitivity = spark.conf.get("spark.sql.caseSensitive")
    if case_sensitive_schema:
        spark.conf.set("spark.sql.caseSensitive", "true")
        # Data Checks here
    display(spark.sql(f"select * from {file_format}.`{target_Path}`"))
    display(spark.sql(f"select count(*) as row_count from {file_format}.`{target_Path}`"))
    # restore session settings
    spark.conf.set("spark.sql.caseSensitive", session_sql_case_sensitivity)



# DBTITLE 1,get_max_column_value
#get_max_column_value
def get_max_column_value(column_name, data_folder_location, file_format="json"):
    """
      get_max_column_value
    """
    max_column_val = None
    max_column_query = f"""
    select max({column_name}) as last_{column_name} from {file_format}.`{data_folder_location}`
  """
    try:
        print(f"INFO: get_max_column_value::  query {max_column_query}")
        rows = spark.sql(max_column_query).collect()
        max_column_val = rows[0][0]
    except:
        pass
    print(f"INFO: max_column_val = {max_column_val}")
    return max_column_val



# DBTITLE 1,trim_sql_comments_udf
import re
from pyspark.sql.functions import udf
# trim_sql_comments
def trim_sql_comments(input_sql):
    '''
      Removes Block and Line comments from input
    '''
    input_with_no_block_comments = re.sub(r'\/\*(\*(?!\/)|[^*])*\*\/', '', input_sql)
    input_with_no_blockandline_comments = "\n".join([re.sub(r'^\s*(--).*', '', line) for line in input_with_no_block_comments.split("\n")])
    return input_with_no_blockandline_comments
# Register the udf
trim_sql_comments_udf = udf(lambda x: trim_sql_comments(x))
