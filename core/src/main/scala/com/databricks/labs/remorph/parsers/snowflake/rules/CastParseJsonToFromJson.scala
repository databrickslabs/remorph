package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors}
import com.databricks.labs.remorph.generators.sql.DataTypeGenerator
import com.databricks.labs.remorph.intermediate._

class CastParseJsonToFromJson extends Rule[LogicalPlan] with TransformationConstructors {
  override def apply(plan: LogicalPlan): Transformation[LogicalPlan] = {
    plan transformAllExpressions { case Cast(CallFunction("PARSE_JSON", Seq(payload)), dt, _, _, _) =>
      DataTypeGenerator.generateDataType(dt).map { dataType =>
        JsonToStructs(payload, Literal(dataType), None)
      }
    }
  }
}
