import json
import streamlit as st  # type: ignore
from ..config.settings import settings
from ..services.spark_service import load_query, fetch_dataframe, save_config_to_delta
from ..utils.pretty_print_configs import create_collapsible_json


def main():
    st.title("Config Manager")
    tab1, tab2 = st.tabs(["Add New Config", "View Existing Configs"])
    with tab1:
        table_form_expander = st.expander("Add a new config")
        with table_form_expander:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                source_catalog = st.text_input("Source Catalog", value="hive_metastore")
            with col2:
                source_schema = st.text_input("Source Schema", value="labs")
            with col3:
                target_catalog = st.text_input("Target Catalog", value="sandbox_db")
            with col4:
                target_schema = st.text_input("Target Schema", value="labs")

            # Initialize tables list
            if "tables" not in st.session_state:
                st.session_state["tables"] = []

            col1, col2 = st.columns(2)
            with col1:
                source_name = st.text_input("Source Table Name")
            with col2:
                target_name = st.text_input("Target Table Name")

            # Column mapping
            st.subheader("Column Mapping")
            column_mapping = []
            num_columns = st.number_input("Number of columns to map", min_value=1, step=1, key="num_columns")
            for i in range(num_columns):
                col1, col2 = st.columns(2)
                with col1:
                    source_column = st.text_input(f"Source Column {i + 1}", key=f"source_column_{i}")
                with col2:
                    target_column = st.text_input(f"Target Column {i + 1}", key=f"target_column_{i}")
                column_mapping.append({"source_name": source_column, "target_name": target_column})

            # Join columns
            st.subheader("Join Columns")
            join_columns = st.text_input("Enter join columns, comma-separated")

            # Column thresholds
            st.subheader("Column Thresholds")
            column_thresholds = []
            num_thresholds = st.number_input("Number of column thresholds", min_value=0, step=1, key="num_thresholds")
            for i in range(num_thresholds):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    column_name = st.text_input(f"Threshold Column {i + 1}", key=f"threshold_column_{i}")
                with col2:
                    upper_bound = st.text_input(f"Upper Bound for {column_name}", key=f"upper_bound_{i}")
                with col3:
                    lower_bound = st.text_input(f"Lower Bound for {column_name}", key=f"lower_bound_{i}")
                with col4:
                    threshold_type = st.selectbox(
                        f"Type for {column_name}", ["int", "float", "string"], key=f"threshold_type_{i}"
                    )
                column_thresholds.append(
                    {
                        "column_name": column_name,
                        "upper_bound": upper_bound,
                        "lower_bound": lower_bound,
                        "type": threshold_type,
                    }
                )

            # Transformations
            st.subheader("Transformations")
            transformations = []
            num_transformations = st.number_input(
                "Number of transformations", min_value=0, step=1, key="num_transformations"
            )
            for i in range(num_transformations):
                col1, col2, col3 = st.columns(3)
                with col1:
                    column_name = st.text_input(f"Column Name {i + 1}", key=f"column_name_{i}")
                with col2:
                    source = st.text_input(f"Transformation Source {i + 1}", key=f"transformation_source_{i}")
                with col3:
                    target = st.text_input(f"Transformation Target {i + 1}", key=f"transformation_target_{i}")
                transformations.append({"column_name": column_name, "source": source, "target": target})

            # Drop columns
            st.subheader("Drop Columns")
            drop_columns = st.text_input("Enter columns to drop, comma-separated")

            # Filters
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            with col1:
                source_filter = st.text_area("Source Filter")
            with col2:
                target_filter = st.text_area("Target Filter")
            filters = {"source": source_filter, "target": target_filter}

            # JDBC Reader Options
            st.subheader("JDBC Reader Options")
            jdbc_reader_options = st.text_area("Enter JDBC reader options as JSON")

            # Table thresholds
            st.subheader("Table Thresholds")
            table_thresholds = st.text_area("Enter table thresholds as JSON")

        table_details = {
            "source_catalog": source_catalog,
            "source_schema": source_schema,
            "target_catalog": target_catalog,
            "target_schema": target_schema,
            "tables": [
                {
                    "source_name": source_name,
                    "target_name": target_name,
                    "column_mapping": column_mapping,
                    "drop_columns": drop_columns.split(",") if drop_columns else [],
                    "filters": filters,
                    "jdbc_reader_options": json.loads(jdbc_reader_options) if jdbc_reader_options else {},
                    "join_columns": join_columns.split(",") if join_columns else [],
                    "select_columns": None,  # This can be updated based on additional user inputs if needed
                    "column_thresholds": column_thresholds,
                    "table_thresholds": json.loads(table_thresholds) if table_thresholds else {},
                    "transformations": transformations,
                }
            ],
        }
        table_details_json = json.dumps(table_details, indent=4)
        view_config, save_config = st.columns(2)
        with view_config:
            if st.button("View Config"):
                st.json(table_details_json)
                st.button("Close")
        with save_config:
            if st.button("Save Config"):
                # save_json(json_data=table_details_json, path=RECON_APP_RESOURCES_DIR)
                save_config_to_delta(table_details=table_details)

    with tab2:
        st.write("View Existing Configs")
        # Fetch existing configs
        fetch_configs = load_query(
            "dmls", "fetch_existing_configs", REMORPH_METADATA_SCHEMA=settings.REMORPH_METADATA_SCHEMA
        )
        configs = fetch_dataframe(fetch_configs)

        # Convert the 'tables' column to a string
        configs['tables'] = configs['tables'].apply(create_collapsible_json)

        # Display the DataFrame
        st.dataframe(configs)


if __name__ == "__main__":
    main()
