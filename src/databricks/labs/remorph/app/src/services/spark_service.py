import streamlit as st  # type: ignore
from databricks.connect.session import DatabricksSession
from pyspark.sql import functions as F
from ..utils.schemas.config_schema import config_schema
from ..utils.query_loader import load_query
from ..config.settings import settings


def create_spark_session(cluster_id):
    spark = DatabricksSession.builder.clusterId(cluster_id).getOrCreate()
    return spark


def save_config_to_delta(table_details):
    existing_df = settings.spark.table(f"{settings.REMORPH_METADATA_SCHEMA}.{settings.RECON_CONFIG_TABLE_NAME}")
    max_config_id = existing_df.agg(F.max("config_id")).collect()[0][0]
    new_config_id = (max_config_id or 0) + 1
    table_details["config_id"] = new_config_id

    df = settings.spark.createDataFrame([table_details], schema=config_schema)
    # df.show(truncate=False)
    try:
        df.write.format("delta").mode("append").saveAsTable(
            f"{settings.REMORPH_METADATA_SCHEMA}." f"{settings.RECON_CONFIG_TABLE_NAME}"
        )
        st.success("Config saved successfully")
    except Exception as e:
        st.error(f"Error saving config: {e}")


def run_ddl(ddl, table_name):
    if settings.spark.catalog.tableExists(table_name):
        pass
    else:
        settings.spark.sql(ddl)
        st.success(f"Table {table_name} created successfully")


def initialize_tables():
    with st.spinner("Ensuring config and status tables are present. May take a while if cluster is not up"):
        try:
            create_config_table_ddl = load_query(
                "ddls",
                "create_config_table",
                RECON_CONFIG_TABLE_NAME=f"{settings.REMORPH_METADATA_SCHEMA}." f"{settings.RECON_CONFIG_TABLE_NAME}",
            )

            create_status_table_ddl = load_query(
                "ddls",
                "create_status_table",
                RECON_JOB_RUN_DETAILS_TABLE_NAME=f"{settings.REMORPH_METADATA_SCHEMA}."
                f"{settings.RECON_JOB_RUN_DETAILS_TABLE_NAME}",
            )

            run_ddl(
                create_config_table_ddl, f"{settings.REMORPH_METADATA_SCHEMA}." f"{settings.RECON_CONFIG_TABLE_NAME}"
            )

            run_ddl(
                create_status_table_ddl,
                f"{settings.REMORPH_METADATA_SCHEMA}." f"{settings.RECON_JOB_RUN_DETAILS_TABLE_NAME}",
            )
        except Exception as e:
            st.error(f'Error creating tables. Please check if "{settings.REMORPH_METADATA_SCHEMA}" schema exists')
            st.error(f"Error: {e}") # FIXME : Remove this logging, it is for development purpose only
            # st.error(
            #     f"Please check if these "
            #     f"tables are present: {settings.RECON_CONFIG_TABLE_NAME} and "
            #     f"{settings.RECON_JOB_RUN_DETAILS_TABLE_NAME}"
            # )
            return
    st.session_state.tables_initialized = True


def initialize_app():
    if "tables_initialized" not in st.session_state:
        initialize_tables()


def fetch_dataframe(sql):
    df = settings.spark.sql(sql).toPandas()
    return df


def fetch_list_from_queries(sql):
    items = [item[0] for item in settings.spark.sql(sql).toPandas().values.tolist()]
    return items or None
