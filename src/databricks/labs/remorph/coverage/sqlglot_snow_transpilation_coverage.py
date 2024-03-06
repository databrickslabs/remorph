from pathlib import Path

import sqlglot
from sqlglot.dialects.databricks import Databricks
from sqlglot.dialects.snowflake import Snowflake

from databricks.labs.remorph.coverage import commons

if __name__ == "__main__":
    input_dir = commons.get_env_var("INPUT_DIR", required=True)
    output_dir = commons.get_env_var("OUTPUT_DIR", required=True)
    sqlglot_version = sqlglot.__version__
    SQLGLOT_COMMIT_HASH = ""  # C0103 pylint

    commons.collect_transpilation_stats(
        "SQLGlot",
        SQLGLOT_COMMIT_HASH,
        sqlglot_version,
        Snowflake,
        Databricks,
        Path(input_dir),
        Path(output_dir),
    )
