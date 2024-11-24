package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.LogicalPlan

abstract class LeafStatement extends Statement {
  override def children: Seq[LogicalPlan] = Seq()
}
