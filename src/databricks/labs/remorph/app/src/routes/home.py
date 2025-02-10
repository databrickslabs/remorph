import streamlit as st  # type: ignore
import streamlit.components.v1 as components  # type: ignore


def main():
    # Title and Introduction
    st.title("🔍 Remorph - Reconcile")
    st.markdown("### A powerful tool for **automated data reconciliation** in Databricks.")

    st.header("What is Reconcile?")
    st.markdown(
        """
        **Reconcile** is an automated **data validation and comparison** tool designed for **verifying the accuracy of migrated data**
        between a **source system** and **Databricks**. It helps identify **discrepancies** in data to ensure **seamless and error-free migrations**.

        **Key Capabilities:**
        - ✅ **Compare** source data (e.g., Snowflake, Oracle) with target data in Databricks.
        - 🔍 **Detect anomalies** such as missing rows, mismatched values, or schema inconsistencies.
        - 🚀 **Scale efficiently** to handle large datasets with optimized performance.
        """
    )

    st.header("How Reconcile Works")
    st.markdown("Below is a **visual representation** of the reconciliation process:")

    mermaid_html = """
    <div class="mermaid">
    flowchart TD
        A(Transpile CLI) --> |Directory| B[Transpile All Files In Directory];
        A --> |File| C[Transpile Single File] ;
        B --> D[List Files];
        C --> E("Sqlglot(transpile)");
        D --> E
        E --> |Parse Error| F(Failed Queries)
        E --> G{Skip Validations}
        G --> |Yes| H(Save Output)
        G --> |No| I{Validate}
        I --> |Success| H
        I --> |Fail| J(Flag, Capture)
        J --> H
    </div>

    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true });
    </script>
    """

    components.html(mermaid_html, height=1000)

    st.markdown(
        """
        The **Reconcile process** works in the following steps:

        1️⃣ **Extract Data**: Fetches data from both the **source system** (e.g., Snowflake, Oracle) and **Databricks target table**.
        2️⃣ **Transform & Normalize**: Applies **data transformations** and aligns schema differences.
        3️⃣ **Compare Data**: Performs **row-level, column-level, and aggregated** comparisons.
        4️⃣ **Generate Report**: Identifies **mismatched records**, missing values, and summary statistics.

        🎯 **Result:** A clear report showing how well the migrated data matches the original source.
        """
    )

    st.header("Why is Data Reconciliation Important?")
    options = {
        "Prevent incorrect reports due to data mismatches": "Reconciliation ensures **accurate insights** by eliminating errors.",
        "Ensure compliance with industry regulations": "Regulatory standards often require **data integrity checks**.",
        "Detect unexpected data loss during migration": "Helps catch missing records **before they impact business decisions**.",
        "Improve trust in the migration process": "Ensures **stakeholders** have confidence in the new system.",
    }

    selected_reason = st.radio("📌 Select a reason to learn more:", list(options.keys()))
    st.success(options[selected_reason])

    st.header("Common Data Reconciliation Challenges")
    st.markdown(
        """
        Even with **automated tools** like Reconcile, data validation presents challenges:

        - ⚠️ **Schema Drift**: Unexpected changes in column types or structures.
        - 🔄 **Data Sync Issues**: Time-lagged data updates leading to inconsistencies.
        - 📉 **Large Data Volume**: Millions of rows requiring optimized comparison techniques.
        - 🔍 **Precision vs. Performance**: Balancing speed with deep data validation.

        Reconcile tackles these challenges with **efficient algorithms, distributed processing, and flexible configurations**.
        """
    )

    st.header("Explore More")
    st.markdown(
        "🔗 **Check out the full project on GitHub:** [Databricks Labs Remorph](https://github.com/databrickslabs/remorph)"
    )

    st.markdown("💡 **Need more details?** Reach out to the community and contribute to the project!")
