import logging
from typing import ClassVar

from sqlglot import expressions as exp

from databricks.labs.remorph.snow.databricks import Databricks

logger = logging.getLogger(__name__)


class DatabricksPreivew(Databricks):
    databricks = Databricks()

    class Generator(databricks.Generator):
        TYPE_MAPPING: ClassVar[dict] = {
            **Databricks.Generator.TYPE_MAPPING,
            exp.DataType.Type.VARIANT: "VARIANT",
        }

        del Databricks.Generator.TRANSFORMS[exp.ParseJSON]

        TRANSFORMS: ClassVar[dict] = {
            **Databricks.Generator.TRANSFORMS,
        }
