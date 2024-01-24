from dataclasses import dataclass

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk.core import Config

logger = get_logger(__file__)


@dataclass
class MorphConfig:
    source: str
    input_sql: str
    output_folder: str | None
    sdk_config: Config | None
    skip_validation: bool = False
    catalog_name: str = "transpiler_test"
    schema_name: str = "convertor_test"

    def __post_init__(self):
        # skip validation is false
        if not self.skip_validation:
            if self.sdk_config is None:
                logger.error("sdk config is required when skip_validation is false")
                raise ValueError("sdk config is required when skip_validation is false")
