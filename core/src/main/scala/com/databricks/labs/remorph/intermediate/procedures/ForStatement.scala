package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.LogicalPlan

// FOR [ variable_name AS ] query ... DO ... END FOR
case class ForStatement(
    variableName: Option[String],
    query: LogicalPlan,
    statements: Seq[LogicalPlan],
    label: Option[String] = None)
    extends Statement {
  override def children: Seq[LogicalPlan] = Seq(query) ++ statements
}
