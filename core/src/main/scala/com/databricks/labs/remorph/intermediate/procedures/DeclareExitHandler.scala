package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

case class DeclareExitHandler(conditionValues: Seq[Expression], handlerAction: LogicalPlan) extends Statement {
  override def children: Seq[LogicalPlan] = Seq(handlerAction)
}
