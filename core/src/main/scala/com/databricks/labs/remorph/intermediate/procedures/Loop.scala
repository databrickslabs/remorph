package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.LogicalPlan

// Executes a series of statements repeatedly.
case class Loop(children: Seq[LogicalPlan], label: Option[String] = None) extends Statement
