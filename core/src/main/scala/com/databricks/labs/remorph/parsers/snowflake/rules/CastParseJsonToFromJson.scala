package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.TranspilerState
import com.databricks.labs.remorph.generators.sql.DataTypeGenerator
import com.databricks.labs.remorph.intermediate._

class CastParseJsonToFromJson extends Rule[LogicalPlan] {
  override def apply(plan: LogicalPlan): LogicalPlan = {
    plan transformAllExpressions { case Cast(CallFunction("PARSE_JSON", Seq(payload)), dt, _, _, _) =>
      val dataType = DataTypeGenerator.generateDataType(dt).runAndDiscardState(TranspilerState())
      JsonToStructs(payload, Literal(dataType), None)
    }
  }
}
