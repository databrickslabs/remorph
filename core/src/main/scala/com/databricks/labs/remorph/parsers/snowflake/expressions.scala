package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.{BooleanType, DataType, Expression, LeafExpression, LogicalPlan, LongType, UnresolvedType}

case class NamedArgumentExpression(key: String, value: Expression) extends Expression {
  override def children: Seq[Expression] = value :: Nil
  override def dataType: DataType = UnresolvedType
}

case class NextValue(sequenceName: String) extends LeafExpression {
  override def dataType: DataType = LongType
}

case class Iff(condition: Expression, thenBranch: Expression, elseBranch: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(condition, thenBranch, elseBranch)
  override def dataType: DataType = thenBranch.dataType
}

// TODO: convert into Like
case class LikeSnowflake(
    expression: Expression,
    patterns: Seq[Expression],
    escape: Option[Expression],
    caseSensitive: Boolean)
    extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class IsInCollection(collection: Seq[Expression], expression: Expression) extends Expression {
  override def children: Seq[Expression] = collection :+ expression
  override def dataType: DataType = BooleanType
}

case class IsInRelation(relation: LogicalPlan, expression: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(expression)
  override def dataType: DataType = BooleanType
}
