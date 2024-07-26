# pylint: disable=all
from pathlib import Path

import sqlglot
from sqlglot.dialects.databricks import Databricks

from databricks.labs.remorph.coverage import commons


def run_coverage(dialect, subfolder):
    input_dir = commons.get_env_var("INPUT_DIR_PARENT", required=True)
    output_dir = commons.get_env_var("OUTPUT_DIR", required=True)
    sqlglot_version = sqlglot.__version__
    SQLGLOT_COMMIT_HASH = ""  # C0103 pylint

    if not input_dir:
        raise ValueError("Environment variable `INPUT_DIR_PARENT` is required")
    if not output_dir:
        raise ValueError("Environment variable `OUTPUT_DIR` is required")

    commons.collect_transpilation_stats(
        "SQLGlot",
        SQLGLOT_COMMIT_HASH,
        sqlglot_version,
        dialect,
        Databricks,
        Path(input_dir) / subfolder,
        Path(output_dir),
    )
