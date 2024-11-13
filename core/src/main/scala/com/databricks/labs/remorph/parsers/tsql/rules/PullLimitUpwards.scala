package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.intermediate._

// TSQL has "SELECT TOP N * FROM .." vs "SELECT * FROM .. LIMIT N", so we fix it here
object PullLimitUpwards extends Rule[LogicalPlan] {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transformUp {
    case Project(Limit(child, limit), exprs) =>
      Limit(Project(child, exprs), limit)
    case Filter(Limit(child, limit), cond) =>
      Limit(Filter(child, cond), limit)
    case Sort(Limit(child, limit), order, global) =>
      Limit(Sort(child, order, global), limit)
    case Offset(Limit(child, limit), offset) =>
      Limit(Offset(child, offset), limit)
  }
}
