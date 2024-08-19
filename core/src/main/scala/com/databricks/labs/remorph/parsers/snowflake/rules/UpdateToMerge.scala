package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.{Assign, LogicalPlan, MergeIntoTable, Rule, UpdateAction, UpdateTable}

class UpdateToMerge extends Rule[LogicalPlan] {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case UpdateTable(target, Some(source), assigns, Some(where), _, _) =>
      val set = assigns.filter(_.isInstanceOf[Assign]).map(_.asInstanceOf[Assign])
      MergeIntoTable(target, source, where, matchedActions = Seq(UpdateAction(None, set)))
  }
}
