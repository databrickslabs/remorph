import streamlit as st  # type: ignore
from ..config.settings import settings
from ..services.spark_service import load_query, fetch_dataframe, fetch_list_from_queries


def main():
    st.title("Reconciliation Metrics")

    # Fetch all distinct users to populate the dropdown
    fetch_users = load_query("dmls", "fetch_users", REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA)
    users = fetch_list_from_queries(fetch_users)
    users = [None] + users if users is not None else [None]

    # Fetch all distinct recon tables to populate the dropdown
    fetch_recon_type = load_query("dmls", "fetch_recon_type", REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA)
    recon_tables = fetch_list_from_queries(fetch_recon_type)
    recon_tables = [None] + recon_tables if recon_tables is not None else [None]

    # Fetch source types to populate the dropdown
    fetch_source_types = load_query(
        "dmls", "fetch_source_types", REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA
    )
    source_types = fetch_list_from_queries(fetch_source_types)
    source_types = [None] + source_types if source_types is not None else [None]

    filter_1, filter_2, filter_3 = st.columns(3)
    with filter_1:
        user_name_filter = st.selectbox("Select User", users, index=0)
    with filter_2:
        recon_table_filter = st.selectbox("Select Recon Type", recon_tables, index=0)
    with filter_3:
        source_type_filter = st.selectbox("Select Source", source_types, index=0)
    print(f'User: {user_name_filter}, Recon Table: {recon_table_filter}, Source Type: {source_type_filter}')

    st.divider()

    fetch_total_failed_runs = load_query(
        "dmls", 'fetch_total_failed_runs', REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA
    )
    total_failed_runs = fetch_dataframe(fetch_total_failed_runs)
    total_failed_runs = (
        len(total_failed_runs.index) if total_failed_runs is not None and not total_failed_runs.empty else 0
    )

    fetch_unique_target_tables_failed = load_query(
        "dmls", 'fetch_unique_target_tables_failed', REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA
    )
    unique_target_tables_failed = fetch_dataframe(fetch_unique_target_tables_failed)
    unique_target_tables_failed = (
        len(unique_target_tables_failed.index)
        if unique_target_tables_failed is not None and not unique_target_tables_failed.empty
        else 0
    )

    fetch_unique_target_tables_successful = load_query(
        "dmls", 'fetch_unique_target_tables_successful', REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA
    )
    unique_target_tables_successful = fetch_dataframe(fetch_unique_target_tables_successful)
    unique_target_tables_successful = (
        len(unique_target_tables_successful.index)
        if unique_target_tables_successful is not None and not unique_target_tables_successful.empty
        else 0
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Failed Runs", total_failed_runs, " - No of failed runs")
    with col2:
        st.metric("Unique Target Tables Failed", unique_target_tables_failed, " - Unique Failed Tables")
    with col3:
        st.metric("Unique Target Tables Successful", unique_target_tables_successful, "Unique Successful")

    st.write("Reconciliation Summary")
    fetch_summary_sql = load_query("dmls", "fetch_summary", REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA)
    summary_df = fetch_dataframe(fetch_summary_sql)
    st.dataframe(summary_df)

    st.write("Schema Comparison Details")
    fetch_schema_comparison_details_sql = load_query(
        "dmls", "fetch_schema_comparison_details", REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA
    )
    df_schema_comparison_details = fetch_dataframe(fetch_schema_comparison_details_sql)
    st.dataframe(df_schema_comparison_details)
