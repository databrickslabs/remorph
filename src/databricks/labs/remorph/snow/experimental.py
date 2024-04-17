import logging
from typing import ClassVar

from sqlglot import expressions as exp

from databricks.labs.remorph.snow import databricks

logger = logging.getLogger(__name__)


class DatabricksExperimental(databricks.Databricks):
    databricks = databricks.Databricks()

    class Generator(databricks.Generator):
        TYPE_MAPPING: ClassVar[dict] = {
            **databricks.Databricks.Generator.TYPE_MAPPING,
            exp.DataType.Type.VARIANT: "VARIANT",
        }

        TRANSFORMS: ClassVar[dict] = {
            **databricks.Databricks.Generator.TRANSFORMS,
        }

        TRANSFORMS.pop(exp.ParseJSON, None)
