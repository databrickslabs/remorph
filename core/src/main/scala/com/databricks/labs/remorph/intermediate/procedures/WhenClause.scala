package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

case class WhenClause(condition: Expression, children: Seq[LogicalPlan]) extends Statement
