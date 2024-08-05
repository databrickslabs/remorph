package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{intermediate => ir}

case class NamedArgumentExpression(key: String, value: ir.Expression) extends ir.Expression {
  override def children: Seq[ir.Expression] = value :: Nil
  override def dataType: ir.DataType = ir.UnresolvedType
}

case class NextValue(sequenceName: String) extends ir.LeafExpression {
  override def dataType: ir.DataType = ir.LongType
}

case class Iff(condition: ir.Expression, thenBranch: ir.Expression, elseBranch: ir.Expression) extends ir.Expression {
  override def children: Seq[ir.Expression] = Seq(condition, thenBranch, elseBranch)
  override def dataType: ir.DataType = thenBranch.dataType
}

// TODO: convert into Like
case class LikeSnowflake(
    expression: ir.Expression,
    patterns: Seq[ir.Expression],
    escape: Option[ir.Expression],
    caseSensitive: Boolean)
    extends ir.LeafExpression {
  override def dataType: ir.DataType = ir.UnresolvedType
}
