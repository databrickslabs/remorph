package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.parsers.intermediate._

object TrapInsertDefaultsAction extends Rule[LogicalPlan] {

  override def apply(plan: LogicalPlan): LogicalPlan = plan transformUp {
    case merge @ MergeIntoTable(_, _, _, _, notMatchedActions, _) =>
      notMatchedActions.collectFirst { case InsertDefaultsAction(_) =>
        throw new IllegalArgumentException(
          "The MERGE action 'INSERT DEFAULT VALUES' is not supported in Databricks SQL")
      }
      merge
    case _ => plan
  }
}
