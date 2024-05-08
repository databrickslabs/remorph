import logging

from sqlglot import expressions as exp

from databricks.labs.remorph.snow import databricks as custom_databricks

logger = logging.getLogger(__name__)


class DatabricksExperimental(custom_databricks.Databricks):
    databricks = custom_databricks.Databricks()

    class Generator(custom_databricks.Databricks.Generator):
        TRANSFORMS = {
            **custom_databricks.Databricks.Generator.TRANSFORMS,
        }
        TRANSFORMS.pop(exp.ParseJSON, None)

        TYPE_MAPPING = {
            **custom_databricks.Databricks.Generator.TYPE_MAPPING,
            exp.DataType.Type.VARIANT: "VARIANT",
        }
