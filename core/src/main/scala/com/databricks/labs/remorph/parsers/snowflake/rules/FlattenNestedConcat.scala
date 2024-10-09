package com.databricks.labs.remorph.parsers.snowflake.rules
import com.databricks.labs.remorph.{intermediate => ir}

/**
 * Flattens nested invocations of CONCAT into a single one. For example, `CONCAT(CONCAT(a, b), CONCAT(c, d))` becomes
 * `CONCAT(a, b, c, d)`.
 */
class FlattenNestedConcat extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): ir.LogicalPlan = {
    plan transformAllExpressions flattenConcat
  }

  // Make the implementation accessible for testing without having to build a full LogicalPlan
  private[rules] def flattenConcat: PartialFunction[ir.Expression, ir.Expression] = { case expression =>
    expression transformUp { case ir.Concat(items) =>
      ir.Concat(items.flatMap {
        case ir.Concat(sub) => sub
        case x => Seq(x)
      })
    }
  }
}
