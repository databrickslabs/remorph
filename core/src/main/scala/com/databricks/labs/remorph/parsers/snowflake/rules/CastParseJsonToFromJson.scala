package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.generators.sql.DataTypeGenerator
import com.databricks.labs.remorph.parsers.intermediate._

class CastParseJsonToFromJson(logical: Generator[LogicalPlan, String]) extends Rule[LogicalPlan] {
  private val ctx = GeneratorContext(logical)
  override def apply(plan: LogicalPlan): LogicalPlan = {
    plan transformAllExpressions { case Cast(CallFunction("PARSE_JSON", Seq(payload)), dt, _, _, _) =>
      val dataType = DataTypeGenerator.generateDataType(ctx, dt)
      JsonToStructs(payload, Literal(dataType), None)
    }
  }
}
