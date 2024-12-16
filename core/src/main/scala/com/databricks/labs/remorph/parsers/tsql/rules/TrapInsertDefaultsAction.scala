package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.{PartialResult, Transformation, TransformationConstructors}
import com.databricks.labs.remorph.intermediate._

case class InsertDefaultsAction(condition: Option[Expression]) extends MergeAction {
  override def children: Seq[Expression] = condition.toSeq
}

object TrapInsertDefaultsAction extends Rule[LogicalPlan] with TransformationConstructors {

  override def apply(plan: LogicalPlan): Transformation[LogicalPlan] = plan transformUp {
    case merge @ MergeIntoTable(_, _, _, _, notMatchedActions, _) =>
      notMatchedActions
        .collectFirst { case InsertDefaultsAction(_) =>
          lift(
            PartialResult(
              merge,
              UnexpectedNode("The MERGE action 'INSERT DEFAULT VALUES' is not supported in Databricks SQL")))
        }
        .getOrElse(ok(merge))
  }
}
