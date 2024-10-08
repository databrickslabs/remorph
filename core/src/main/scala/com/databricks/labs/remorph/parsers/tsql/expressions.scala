package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate._

// Specialized function calls, such as XML functions that usually apply to columns
case class TsqlXmlFunction(function: CallFunction, column: Expression) extends Binary(function, column) {
  override def dataType: DataType = UnresolvedType
}

case class Money(value: Literal) extends Unary(value) {
  override def dataType: DataType = UnresolvedType
}

case class Deleted(selection: Expression) extends Unary(selection) {
  override def dataType: DataType = selection.dataType
}

case class Inserted(selection: Expression) extends Unary(selection) {
  override def dataType: DataType = selection.dataType
}

// The default case for the expression parser needs to be explicitly defined to distinguish [DEFAULT]
case class Default() extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}
