package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.{intermediate => ir}

case class NamedArgumentExpression(key: String, value: ir.Expression) extends ir.Expression {
  override def children: Seq[ir.Expression] = value :: Nil
  override def dataType: ir.DataType = value.dataType
}

case class NextValue(sequenceName: String) extends ir.LeafExpression {
  override def dataType: ir.DataType = ir.LongType
}