package com.databricks.labs.remorph.parsers.intermediate

// Used for DML other than SELECT
abstract class Modification extends LogicalPlan

case class InsertIntoTable( // TODO: fix it
    target: LogicalPlan,
    columns: Option[Seq[Id]],
    values: LogicalPlan,
    outputRelation: Option[LogicalPlan],
    options: Option[Expression],
    overwrite: Boolean)
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, values, outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class DeleteFromTable(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    where: Option[Expression],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class UpdateTable(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    set: Seq[Expression],
    where: Option[Expression],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class MergeTables(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    conditions: Option[Expression],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}
