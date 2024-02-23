from pathlib import Path

import commons
import sqlglot
from sqlglot.dialects.databricks import Databricks
from sqlglot.dialects.snowflake import Snowflake

if __name__ == "__main__":
    input_dir = commons.get_env_var("INPUT_DIR", required=True)
    output_dir = commons.get_env_var("OUTPUT_DIR", required=True)
    sqlglot_version = sqlglot.__version__
    sqlglot_commit_hash = ""

    commons.collect_transpilation_stats(
        "SQLGlot",
        sqlglot_commit_hash,
        sqlglot_version,
        Snowflake,
        Databricks,
        Path(input_dir),
        Path(output_dir),
    )
