from pathlib import Path

import coverage_utils

from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow

if __name__ == "__main__":
    input_dir = coverage_utils.get_env_var("INPUT_DIR", required=True)
    output_dir = coverage_utils.get_env_var("OUTPUT_DIR", required=True)

    remorph_commit_hash = coverage_utils.get_current_commit_hash() or ""
    remorph_version = ""

    coverage_utils.collect_transpilation_stats(
        "Remorph",
        remorph_commit_hash,
        remorph_version,
        Snow,
        Databricks,
        Path(input_dir),
        Path(output_dir),
    )
