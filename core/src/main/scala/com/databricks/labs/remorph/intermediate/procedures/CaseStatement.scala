package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.LogicalPlan

// there's Switch(..) node in this package just to represent a case statement with value match. Theoretically,
// we can merge these two, but semantics are clearer this way.
case class CaseStatement(when: Seq[WhenClause], orElse: Seq[LogicalPlan] = Seq.empty) extends Statement {
  override def children: Seq[LogicalPlan] = when ++ orElse
}
