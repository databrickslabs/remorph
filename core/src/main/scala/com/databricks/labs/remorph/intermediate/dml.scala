package com.databricks.labs.remorph.intermediate

// Used for DML other than SELECT
abstract class Modification extends LogicalPlan

case class InsertIntoTable(
    target: LogicalPlan,
    columns: Option[Seq[NameOrPosition]],
    values: LogicalPlan,
    outputRelation: Option[LogicalPlan] = None,
    options: Option[Expression] = None,
    overwrite: Boolean = false)
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, values, outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class DeleteFromTable(
    target: LogicalPlan,
    source: Option[LogicalPlan] = None,
    where: Option[Expression] = None,
    outputRelation: Option[LogicalPlan] = None,
    options: Option[Expression] = None)
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class UpdateTable(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    set: Seq[Expression],
    where: Option[Expression] = None,
    outputRelation: Option[LogicalPlan] = None,
    options: Option[Expression] = None)
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

/**
 * The logical plan of the MERGE INTO command, aligned with SparkSQL
 */
case class MergeIntoTable(
    targetTable: LogicalPlan,
    sourceTable: LogicalPlan,
    mergeCondition: Expression,
    matchedActions: Seq[MergeAction] = Seq.empty,
    notMatchedActions: Seq[MergeAction] = Seq.empty,
    notMatchedBySourceActions: Seq[MergeAction] = Seq.empty)
    extends Modification {

  override def children: Seq[LogicalPlan] = Seq(targetTable, sourceTable)
  override def output: Seq[Attribute] = targetTable.output
}

abstract class MergeAction extends Expression {
  def condition: Option[Expression]
  override def dataType: DataType = UnresolvedType
  override def children: Seq[Expression] = condition.toSeq
}

case class DeleteAction(condition: Option[Expression] = None) extends MergeAction

case class UpdateAction(condition: Option[Expression], assignments: Seq[Assign]) extends MergeAction {
  override def children: Seq[Expression] = condition.toSeq ++ assignments
}

case class InsertAction(condition: Option[Expression], assignments: Seq[Assign]) extends MergeAction {
  override def children: Seq[Expression] = assignments
}
