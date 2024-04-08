import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MorphConfig:
    __file__ = "config.yml"
    __version__ = 1

    source: str
    sdk_config: dict[str, str] | None = None
    input_sql: str | None = None
    output_folder: str | None = None
    skip_validation: bool = False
    catalog_name: str = "transpiler_test"
    schema_name: str = "convertor_test"
