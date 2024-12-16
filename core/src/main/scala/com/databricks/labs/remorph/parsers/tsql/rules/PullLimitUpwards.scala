package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors}
import com.databricks.labs.remorph.intermediate._

// TSQL has "SELECT TOP N * FROM .." vs "SELECT * FROM .. LIMIT N", so we fix it here
object PullLimitUpwards extends Rule[LogicalPlan] with TransformationConstructors {
  override def apply(plan: LogicalPlan): Transformation[LogicalPlan] = plan transformUp {
    case Project(Limit(child, limit), exprs) =>
      ok(Limit(Project(child, exprs), limit))
    case Filter(Limit(child, limit), cond) =>
      ok(Limit(Filter(child, cond), limit))
    case Sort(Limit(child, limit), order, global) =>
      ok(Limit(Sort(child, order, global), limit))
    case Offset(Limit(child, limit), offset) =>
      ok(Limit(Offset(child, offset), limit))
  }
}
