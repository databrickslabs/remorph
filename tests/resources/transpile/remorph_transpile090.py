# Installs the latest released version of the databricks-labs-remorph library.
# %pip install databricks-labs-remorph
# dbutils.library.restartPython()

# Import necessary classes from the databricks SDK and remorph library
from databricks.sdk import WorkspaceClient
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.transpiler import execute

# This cell sets up the necessary configuration parameters for the remorph transpilation process.
# Please provide the catalog_name,schema_name,source_dialect,input_source,output_folder.

catalog_name = "remorph"  # provide catalog name for remorph
schema_name = "default"  # provide schema name for remorph
source_dialect = "snowflake"  # Provide source dialect
input_source = "/Workspace/Users/sriram.mohanty@databricks.com/snowflake/input_sql/"  # Provide input folder path which contains the DDLs
output_folder = "/Workspace/Users/sriram.mohanty@databricks.com/snowflake/converted_sql/"  # Output folder path
skip_validation = True  # Skip validation : generated queries are validated syntactically.To validate a query the table definations should be present.Hence for all the DDLs skip_validation will be always false.

# Initialize the WorkspaceClient with the specified product and version and TranspileConfig object with the provided configuration parameters.
wsclient = WorkspaceClient(product="remorph", product_version="0.9.0")
mrophconfig = MorphConfig(
    source=source_dialect,
    input_sql=input_source,
    output_folder=output_folder,
    catalog_name=catalog_name,
    schema_name=schema_name,
)


status = execute.morph(workspace_client=wsclient, config=mrophconfig)
# display(status)
# Please check output_folder for the converted DDLs
