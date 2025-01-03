package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

// CASE toMatch WHEN x THEN y WHEN z THEN a ELSE b END CASE
case class Switch(toMatch: Expression, when: Seq[WhenClause], orElse: Seq[LogicalPlan] = Seq.empty) extends Statement {
  override def children: Seq[LogicalPlan] = when ++ orElse
}
