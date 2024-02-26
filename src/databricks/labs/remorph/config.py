import logging
from dataclasses import dataclass

from databricks.sdk.core import Config

logger = logging.getLogger(__name__)


@dataclass
class MorphConfig:
    __file__ = "config.yml"
    __version__ = 1

    source: str
    sdk_config: Config | None
    input_sql: str | None = None
    output_folder: str | None = None
    skip_validation: bool = False
    catalog_name: str = "transpiler_test"
    schema_name: str = "convertor_test"

    def __post_init__(self):
        # skip validation is false
        if not self.skip_validation:
            if self.sdk_config is None:
                logger.error("sdk config is required when skip_validation is false")
                raise ValueError("sdk config is required when skip_validation is false")
