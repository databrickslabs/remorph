package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

case class ElseIf(condition: Expression, children: Seq[LogicalPlan]) extends Statement
