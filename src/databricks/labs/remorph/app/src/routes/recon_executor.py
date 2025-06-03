import streamlit as st  # type: ignore


def load_configurations():
    # This function should load available configurations
    # For demonstration, we use a static list
    return ["Config 1", "Config 2", "Config 3"]


def run_reconciliation(selected_config):
    # This function should run the reconciliation process based on the selected configuration
    st.success(f"Running reconciliation with {selected_config}")


def main():
    st.title("Recon Executor")
    st.markdown("### W.I.P")

    # Load available configurations
    configurations = load_configurations()

    # Select a configuration
    selected_config = st.selectbox("Choose a configuration", configurations)

    # Button to run reconciliation
    if st.button("Run Reconciliation"):
        run_reconciliation(selected_config)


if __name__ == "__main__":
    main()
