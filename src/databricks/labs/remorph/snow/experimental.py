import logging

from sqlglot import expressions as exp

from databricks.labs.remorph.snow import databricks as extended_databricks

logger = logging.getLogger(__name__)


class DatabricksExperimental(extended_databricks.Databricks):
    databricks = extended_databricks.Databricks()

    class Generator(extended_databricks.Databricks.Generator):
        TRANSFORMS = {
            **extended_databricks.Databricks.Generator.TRANSFORMS,
        }
        TRANSFORMS.pop(exp.ParseJSON, None)

        TYPE_MAPPING = {
            **extended_databricks.Databricks.Generator.TYPE_MAPPING,
            exp.DataType.Type.VARIANT: "VARIANT",
        }
