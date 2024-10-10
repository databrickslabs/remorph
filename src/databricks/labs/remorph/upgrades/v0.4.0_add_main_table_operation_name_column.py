# pylint: disable=invalid-name
import logging
import re
from importlib.resources import files

import databricks.labs.remorph.resources

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.deployment.recon import RECON_JOB_NAME
from databricks.labs.remorph.helpers import db_sql

logger = logging.getLogger(__name__)


def _replace_patterns(sql_text: str) -> str:
    """
    Replace the STRUCT and MAP datatypes in the SQL text with empty string
    """
    parsed_sql_text = sql_text
    for pattern in (r'STRUCT<.*?>', r'MAP<.*?>'):
        parsed_sql_text = re.sub(pattern, "", parsed_sql_text, flags=re.DOTALL)
    return parsed_sql_text


def _extract_columns_with_datatype(sql_text: str) -> list[str]:
    """
    Extract the columns with datatype from the SQL text
    Example:
        Input: CREATE TABLE main (
            recon_table_id BIGINT NOT NULL,
            report_type STRING NOT NULL
            );
       Output:  [recon_table_id BIGINT NOT NULL,
                      report_type STRING NOT NULL]
    """
    return sql_text[sql_text.index("(") + 1 : sql_text.index(")")].strip().split(",")


def _extract_column_name(column_with_datatype: str) -> str:
    """
    Extract the column name from the column with datatype.
    Example:
        Input: \n    recon_table_id BIGINT NOT NULL,
        Output: recon_table_id
    """
    return column_with_datatype.strip("\n").strip().split(" ")[0]


def _main_table_query() -> str:
    """
    Get the main table DDL from the main.sql file
    :return: str
    """
    resources = files(databricks.labs.remorph.resources)
    query_dir = resources.joinpath("reconcile/queries/installation")
    return query_dir.joinpath("main.sql").read_text()


def _current_main_table_columns() -> list[str]:
    """
    Extract the column names from the main table DDL
    :return: column_names: list[str]
    """
    main_sql = _replace_patterns(_main_table_query())
    main_table_columns = [
        _extract_column_name(main_table_column) for main_table_column in _extract_columns_with_datatype(main_sql)
    ]
    return main_table_columns


def _installed_main_table_columns(ws: WorkspaceClient, table_identifier: str) -> list[str]:
    """
    Fetch the column names from the installed table on Databricks Workspace using SQL Backend
    :return: column_names: list[str]
    """
    main_table_columns = list(db_sql.get_sql_backend(ws).fetch(f"DESC {table_identifier}"))
    return [row.col_name for row in main_table_columns]


def _main_table_mismatch(installed_main_table_columns, current_main_table_columns) -> bool:
    # Compare the current main table columns with the installed main table columns
    mismatch = False
    if "operation_name" in installed_main_table_columns and len(installed_main_table_columns) != len(
        current_main_table_columns
    ):
        mismatch = True
    if sorted(installed_main_table_columns) != sorted(current_main_table_columns):
        mismatch = True
    return mismatch


def _recreate_main_table_sql(
    table_identifier: str,
    installed_main_table_columns: list[str],
    current_main_table_columns: list[str],
    prompts: Prompts,
) -> str | None:
    """
    * Verify all the current main table columns are present in the installed main table and then use CTAS to recreate the main table
       * If any of the current main table columns are missing in the installed main table, prompt the user to recreate the main table:
            - If the user confirms, recreate the main table using the main DDL file, else log an error message and exit
    :param table_identifier:
    :param installed_main_table_columns:
    :param current_main_table_columns:
    :param prompts:
    :return:
    """
    sql: str | None = (
        f"CREATE OR REPLACE TABLE {table_identifier} AS SELECT {','.join(current_main_table_columns)} FROM {table_identifier}"
    )

    if not set(current_main_table_columns).issubset(installed_main_table_columns):
        if prompts.confirm("The `main` table columns are not as expected. Do you want to recreate the `main` table?"):
            sql = _main_table_query()
        else:
            logger.error("The `main` table columns are not as expected. Please check and recreate the `main` table.")
            sql = None
    return sql


def _upgrade_reconcile_metadata_main_table(
    installation: Installation,
    ws: WorkspaceClient,
    app_context: ApplicationContext,
):
    """
    Add operation_name column to the main table as part of the upgrade process.
    - Compare the current main table columns with the installed main table columns. If there is any mismatch:
       * Verify all the current main table columns are present in the installed main table and then use CTAS to recreate the main table
       * If any of the current main table columns are missing in the installed main table, prompt the user to recreate the main table:
            - If the user confirms, recreate the main table using the main DDL file, else log an error message and exit
    :param installation:
    :param ws:
    :param app_context:
    """
    reconcile_config = app_context.recon_config
    assert reconcile_config, "Reconcile config must be present to upgrade the reconcile metadata main table"
    table_identifier = f"{reconcile_config.metadata_config.catalog}.{reconcile_config.metadata_config.schema}.main1"
    installed_main_table_columns = _installed_main_table_columns(ws, table_identifier)
    sql: str | None = f"ALTER TABLE {table_identifier} ADD COLUMN operation_name  STRING AFTER report_type"
    if _main_table_mismatch(installed_main_table_columns, _current_main_table_columns()):
        logger.info("Recreating main table")
        sql = _recreate_main_table_sql(
            table_identifier, installed_main_table_columns, _current_main_table_columns(), app_context.prompts
        )
    if sql:
        logger.debug(f"Executing SQL to upgrade main table: \n{sql}")
        db_sql.get_sql_backend(ws).execute(sql)
        installation.save(reconcile_config)
        logger.debug("Upgraded Reconcile main table")


def _upgrade_reconcile_workflow(app_context: ApplicationContext):
    if app_context.recon_config:
        logger.info("Upgrading reconcile workflow")
        wheels = app_context.product_info.wheels(app_context.workspace_client)
        wheel_path = f"/Workspace{wheels.upload_to_wsfs()}"
        app_context.job_deployment.deploy_recon_job(RECON_JOB_NAME, app_context.recon_config, wheel_path)
        logger.debug("Upgraded reconcile workflow")


def upgrade(installation: Installation, ws: WorkspaceClient):
    app_context = ApplicationContext(ws)
    _upgrade_reconcile_metadata_main_table(installation, ws, app_context)
    _upgrade_reconcile_workflow(app_context)
