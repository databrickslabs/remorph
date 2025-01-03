package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.LogicalPlan

// aka BEGIN ... END
case class CompoundStatement(children: Seq[LogicalPlan], label: Option[String] = None) extends Statement
