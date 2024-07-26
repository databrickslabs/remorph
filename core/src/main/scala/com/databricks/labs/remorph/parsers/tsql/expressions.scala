package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate._

// Specialized function calls, such as XML functions that usually apply to columns
case class XmlFunction(function: CallFunction, column: Expression) extends Binary(function, column) {
  override def dataType: DataType = UnresolvedType
}

case class Money(value: Literal) extends Unary(value) {
  override def dataType: DataType = UnresolvedType
}
