package com.databricks.labs.remorph.parsers.snowflake.rules
import com.databricks.labs.remorph.{Transformation, TransformationConstructors, intermediate => ir}

/**
 * Flattens nested invocations of CONCAT into a single one. For example, `CONCAT(CONCAT(a, b), CONCAT(c, d))` becomes
 * `CONCAT(a, b, c, d)`.
 */
class FlattenNestedConcat extends ir.Rule[ir.LogicalPlan] with TransformationConstructors {

  override def apply(plan: ir.LogicalPlan): Transformation[ir.LogicalPlan] = {
    plan transformAllExpressions flattenConcat
  }

  // Make the implementation accessible for testing without having to build a full LogicalPlan
  private[rules] def flattenConcat: PartialFunction[ir.Expression, Transformation[ir.Expression]] = { case expression =>
    expression transformUp { case ir.Concat(items) =>
      ok(ir.Concat(items.flatMap {
        case ir.Concat(sub) => sub
        case x => Seq(x)
      }))
    }
  }
}
