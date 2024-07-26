package com.databricks.labs.remorph.parsers.intermediate

// Unary arithmetic expressions
case class UMinus(expression: Expression) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}
case class UPlus(expression: Expression) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}

// Binary Arithmetic expressions
case class Multiply(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Divide(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Mod(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Add(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Subtract(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
