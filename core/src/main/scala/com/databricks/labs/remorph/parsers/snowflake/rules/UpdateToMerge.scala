package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors}
import com.databricks.labs.remorph.intermediate.{Assign, Expression, Join, LogicalPlan, MergeAction, MergeIntoTable, Noop, NoopNode, Rule, UpdateAction, UpdateTable}

class UpdateToMerge extends Rule[LogicalPlan] with TransformationConstructors {
  override def apply(plan: LogicalPlan): Transformation[LogicalPlan] = plan transform {
    case update @ UpdateTable(_, None, _, _, _, _) => ok(update)
    case update: UpdateTable =>
      ok(MergeIntoTable(update.target, source(update), condition(update), matchedActions = matchedActions(update)))
  }

  private def matchedActions(update: UpdateTable): Seq[MergeAction] = {
    val set = update.set.collect { case a: Assign => a }
    Seq(UpdateAction(None, set))
  }

  private def source(update: UpdateTable): LogicalPlan = update.source match {
    case Some(plan) =>
      plan match {
        case Join(_, source, _, _, _, _) =>
          // TODO: figure out why there's a join in the update plan
          source
        case _ => plan
      }
    case None => NoopNode
  }

  private def condition(update: UpdateTable): Expression = update.where match {
    case Some(condition) => condition
    case None => Noop
  }
}
