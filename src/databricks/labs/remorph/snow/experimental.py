import logging
from sqlglot import expressions as exp

from databricks.labs.remorph.snow import databricks as extended_databricks

logger = logging.getLogger(__name__)


class DatabricksExperimental(extended_databricks.Databricks):
    databricks = extended_databricks.Databricks()

    class Generator(extended_databricks.Databricks.Generator):
        def _parse_json(self, expression: exp.ParseJSON) -> str:
            return self.func("PARSE_JSON", expression.this, expression.expression)

        TRANSFORMS = {
            **extended_databricks.Databricks.Generator.TRANSFORMS,
            exp.ParseJSON: _parse_json,
        }

        TYPE_MAPPING = {
            **extended_databricks.Databricks.Generator.TYPE_MAPPING,
            exp.DataType.Type.VARIANT: "VARIANT",
        }
