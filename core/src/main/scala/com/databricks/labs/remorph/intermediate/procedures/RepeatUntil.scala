package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

// Executes a series of statements repeatedly until the loop-terminating condition is satisfied.
case class RepeatUntil(condition: Expression, children: Seq[LogicalPlan], label: Option[String] = None)
    extends Statement
