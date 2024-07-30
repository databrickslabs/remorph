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

/**
 * The logical plan of the MERGE INTO command, aligned with SparkSQL
 */
case class MergeIntoTable(
    target: LogicalPlan,
    source: LogicalPlan,
    mergeCondition: Expression,
    matchedActions: Seq[MergeAction],
    notMatchedActions: Seq[MergeAction],
    notMatchedBySourceActions: Seq[MergeAction],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {

  override def children: Seq[LogicalPlan] = {
    val notMatchedValues = notMatchedActions.collect { case insertAction: InsertAction =>
      insertAction.values
    }
    Seq(target, source) ++ outputRelation ++ notMatchedValues
  }
  override def output: Seq[Attribute] = target.output
}

sealed abstract class MergeAction extends Expression {
  def condition: Option[Expression]
  override def dataType: DataType = UnresolvedType
  override def children: Seq[Expression] = condition.toSeq
}

case class DeleteAction(condition: Option[Expression]) extends MergeAction

case class UpdateAction(condition: Option[Expression], assignments: Seq[Expression]) extends MergeAction {
  override def children: Seq[Expression] = condition.toSeq ++ assignments
}

case class UpdateStarAction(condition: Option[Expression]) extends MergeAction {
  override def children: Seq[Expression] = condition.toSeq
}

// TODO: As per Insert Above, the columns and values should perhaps become assignments to match Spark,
// but TSql allows INSERT from derived rows, so this may be a better representation.
case class InsertAction(condition: Option[Expression], columns: Option[Seq[Id]], values: LogicalPlan)
    extends MergeAction {
  override def children: Seq[Expression] = values.expressions
}

case class InsertStarAction(condition: Option[Expression]) extends MergeAction {
  override def children: Seq[Expression] = condition.toSeq
}
