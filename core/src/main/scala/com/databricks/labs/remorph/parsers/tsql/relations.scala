package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate._

case class DerivedRows(rows: Seq[Seq[Expression]]) extends LeafNode {
  override def output: Seq[Attribute] = rows.flatten.map(e => AttributeReference(e.toString, e.dataType))
}

case class Output(target: Option[LogicalPlan], outputs: Seq[Expression], columns: Option[Seq[Column]])
    extends RelationCommon {
  override def output: Seq[Attribute] = outputs.map(e => AttributeReference(e.toString, e.dataType))
  override def children: Seq[LogicalPlan] = Seq(target.getOrElse(NoopNode))
}

case class WithOutputClause(input: LogicalPlan, target: LogicalPlan) extends Modification {
  override def output: Seq[Attribute] = target.output
  override def children: Seq[LogicalPlan] = Seq(input, target)
}

case class BackupDatabase(
    databaseName: String,
    disks: Seq[String],
    flags: Map[String, Boolean],
    autoFlags: Seq[String],
    values: Map[String, Expression])
    extends Catalog {}

case class ColumnAliases(input: LogicalPlan, aliases: Seq[Id]) extends RelationCommon {
  override def output: Seq[Attribute] = aliases.map(a => AttributeReference(a.id, StringType))
  override def children: Seq[LogicalPlan] = Seq(input)
}

case class DefaultValues() extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}
