import logging
from typing import ClassVar

from sqlglot import expressions as exp

from databricks.labs.remorph.snow import databricks as custom_databricks

logger = logging.getLogger(__name__)


class DatabricksExperimental(custom_databricks.Databricks):
    databricks = custom_databricks.Databricks()

    class Generator(custom_databricks.Databricks.Generator):
        def __init__(self):
            super().__init__()
            self.TRANSFORMS: ClassVar[dict] = {
                **custom_databricks.Databricks.Generator.TRANSFORMS,
            }
            self.TRANSFORMS.pop(exp.ParseJSON, None)

            self.TYPE_MAPPING: ClassVar[dict] = {
                **custom_databricks.Databricks.Generator.TYPE_MAPPING,
                exp.DataType.Type.VARIANT: "VARIANT",
            }
