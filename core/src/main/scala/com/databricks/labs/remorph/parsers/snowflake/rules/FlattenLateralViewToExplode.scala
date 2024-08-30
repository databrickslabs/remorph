package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.NamedArgumentExpression

// @see https://docs.snowflake.com/en/sql-reference/functions/flatten
class FlattenLateralViewToExplode extends Rule[LogicalPlan] with IRHelpers {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case l @ Join(Lateral(TableFunction(CallFunction("FLATTEN", args)), _), right, _, _, _, _) =>
      l
    case l @ Join(left, Lateral(TableFunction(CallFunction("FLATTEN", args)), _), _, _, _, _) =>
      l
    case Lateral(TableFunction(CallFunction("FLATTEN", args)), _) =>
      val named = args.collect { case NamedArgumentExpression(key, value) =>
        key.toUpperCase() -> value
      }.toMap
      val input = named("INPUT")
      // val path = named.get("PATH").orElse(Some(Literal("")))
      val outer = getFlag(named, "OUTER")
      // val recursive = getFlag(named, "RECURSIVE")
      // val mode = named.get("MODE").orElse(Some(Literal("BOTH")))
      val explode = Explode(input)
      Lateral(TableFunction(explode), outer = outer)
  }

  private def getFlag(named: Map[String, Expression], flagName: String): Boolean = named.get(flagName) match {
    case Some(BooleanLiteral(value)) => value
    case _ => false
  }
}
