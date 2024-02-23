from pathlib import Path

import commons
from databricks.labs.blueprint.wheels import ProductInfo

from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow

if __name__ == "__main__":
    input_dir = commons.get_env_var("INPUT_DIR", required=True)
    output_dir = commons.get_env_var("OUTPUT_DIR", required=True)

    remorph_commit_hash = commons.get_current_commit_hash() or ""
    product_info = ProductInfo(__file__)
    remorph_version = product_info.unreleased_version()

    commons.collect_transpilation_stats(
        "Remorph",
        remorph_commit_hash,
        remorph_version,
        Snow,
        Databricks,
        Path(input_dir),
        Path(output_dir),
    )
