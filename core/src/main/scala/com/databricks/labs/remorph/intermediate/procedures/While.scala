package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

// Continuously executes a list of statements as long as a specified condition remains true.
case class While(condition: Expression, children: Seq[LogicalPlan], label: Option[String] = None) extends Statement
