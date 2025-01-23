# This is an example python code which can be used to perform reconciliation using remorph in Databricks notebook.
# %pip install git+https://github.com/databrickslabs/remorph
# dbutils.library.restartPython()
from databricks.sdk import WorkspaceClient
from pyspark.shell import spark

from databricks.labs.remorph.config import ReconcileConfig, DatabaseConfig, ReconcileMetadataConfig
from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.exception import ReconciliationException
from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.reconcile.execute import reconcile_aggregates
from databricks.labs.remorph.reconcile.recon_config import Table, ColumnMapping, Aggregate

# Create a workspace client
ws = WorkspaceClient(product="remorph", product_version="0.9.0")

source_catalog = ""  # Provide the source catalog name ex: hive_metastore
source_schema = ""  # Provide the source schema name ex: default
target_catalog = ""  # Provide the target catalog name ex: users
target_schema = ""  # Provide the target schema name ex: remorph

# Configure recon source and target
reconcile_config = ReconcileConfig(
    data_source="databricks",  # provide the data source name ex: snowflake
    report_type="row",  # schema,row,data or all https://github.com/databrickslabs/remorph/tree/main/docs/recon_configurations#types-of-report-supported
    secret_scope="remorph_databricks",
    database_config=DatabaseConfig(
        source_catalog=source_catalog,
        source_schema=source_schema,
        target_catalog=target_catalog,
        target_schema=target_schema,
    ),
    metadata_config=ReconcileMetadataConfig(catalog=target_catalog, schema=target_schema),
)


# Table recon configuration
table_recon = TableRecon(
    source_schema=source_schema,
    target_catalog=target_catalog,
    target_schema=target_schema,
    tables=[
        Table(
            source_name="source_employee_table",  # Provide the source table name
            target_name="target_employee_table",  # Provide the target table name
            column_mapping=[
                ColumnMapping(source_name="emp_id", target_name="employee_id"), # Provide the source and target column name if they have different names
                ColumnMapping(source_name="salary", target_name="sal"),
            ],
            join_columns=["emp_id"],  # for recon type all join_columns is mandatory
        ),
        Table(source_name="source_dept_table", target_name="target_dept_table", join_columns=["dept_id"]),
    ],
)


# Performing reconciliation
try:
    result = recon(ws, spark, table_recon, reconcile_config)
    print(f" Success : {result.recon_id}")
    print("***************************")
except ReconciliationException as e:
    print(f"Exception : {str(e)}")
    print("***************************")
except Exception as e:
    print(f"Exception : {str(e)}")
    print("***************************")


# Check target_catalog.target_schema.details table for the reconciliation report

# Table configuration for aggregated reconciliation
table_recon_agg = TableRecon(
    source_schema=source_schema,
    target_catalog=target_catalog,
    target_schema=target_schema,
    tables=[
        Table(
            source_name="source_employee_table",
            target_name="target_employee_table",
            aggregates=[
                Aggregate(
                    agg_columns=["emp_id"], type="count"
                ),  # Provide the column name and aggregation type https://github.com/databrickslabs/remorph/tree/main/docs/recon_configurations#supported-aggregate-functions
                Aggregate(agg_columns=["salary"], type="min"),
                Aggregate(agg_columns=["salary"], type="max"),
            ],
            join_columns=["emp_id"],  # for recon type all join_columns is mandatory
        ),
    ],
)

try:
    result = reconcile_aggregates(ws, spark, table_recon_agg, reconcile_config)  # _aggregates
    recon_id = result.recon_id
    print(f" Success : {recon_id}")
    print("***************************")
except ReconciliationException as e:
    print(f"Exception : {str(e)}")
    print("***************************")
except Exception as e:
    print(f"Exception : {str(e)}")
    print("***************************")

# Check target_catalog.target_schema.aggregate_details table for the aggregated reconciliation
