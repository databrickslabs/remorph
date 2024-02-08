from dataclasses import dataclass

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient

logger = get_logger(__file__)


@dataclass
class MorphConfig:
    source: str
    input_sql: str
    output_folder: str | None
    sdk_client: WorkspaceClient | None
    skip_validation: bool = False
    serverless_warehouse_id: str = None
    catalog_name: str = "transpiler_test"
    schema_name: str = "convertor_test"

    def __post_init__(self):
        # skip validation is false
        if not self.skip_validation:
            if self.sdk_client.config is None:
                logger.error("sdk config is required when skip_validation is false")
                raise ValueError("sdk config is required when skip_validation is false")
