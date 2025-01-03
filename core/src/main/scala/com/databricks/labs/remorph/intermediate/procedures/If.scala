package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Expression, LogicalPlan}

case class If(
    condition: Expression,
    thenDo: Seq[LogicalPlan],
    elseIf: Seq[ElseIf] = Seq.empty,
    orElse: Seq[LogicalPlan] = Seq.empty)
    extends Statement {
  override def children: Seq[LogicalPlan] = thenDo ++ elseIf ++ orElse
}
