package com.databricks.labs.remorph.parsers.intermediate

trait Predicate extends AstExtension {
  def dataType: DataType = BooleanType
}

case class And(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class Or(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class Not(pred: Expression) extends Unary(pred) with Predicate

case class Equals(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class NotEquals(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class LessThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class LessThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class GreaterThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate
case class GreaterThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate

trait Bitwise

// Bitwise NOT is highest precedence after parens '(' ')'
case class BitwiseNot(expression: Expression) extends Unary(expression) with Bitwise {
  override def dataType: DataType = expression.dataType
}

// Binary bitwise expressions
case class BitwiseAnd(left: Expression, right: Expression) extends Binary(left, right) with Bitwise {
  override def dataType: DataType = left.dataType
}

case class BitwiseOr(left: Expression, right: Expression) extends Binary(left, right) with Bitwise {
  override def dataType: DataType = left.dataType
}

case class BitwiseXor(left: Expression, right: Expression) extends Binary(left, right) with Bitwise {
  override def dataType: DataType = left.dataType
}

trait Arithmetic

// Unary arithmetic expressions
case class UMinus(expression: Expression) extends Unary(expression) with Arithmetic {
  override def dataType: DataType = expression.dataType
}

case class UPlus(expression: Expression) extends Unary(expression) with Arithmetic {
  override def dataType: DataType = expression.dataType
}

// Binary Arithmetic expressions
case class Multiply(left: Expression, right: Expression) extends Binary(left, right) with Arithmetic {
  override def dataType: DataType = left.dataType
}

case class Divide(left: Expression, right: Expression) extends Binary(left, right) with Arithmetic {
  override def dataType: DataType = left.dataType
}

case class Mod(left: Expression, right: Expression) extends Binary(left, right) with Arithmetic {
  override def dataType: DataType = left.dataType
}

case class Add(left: Expression, right: Expression) extends Binary(left, right) with Arithmetic {
  override def dataType: DataType = left.dataType
}

case class Subtract(left: Expression, right: Expression) extends Binary(left, right) with Arithmetic {
  override def dataType: DataType = left.dataType
}

/**
 * str like pattern[ ESCAPE escape] - Returns true if str matches `pattern` with `escape`, null if any arguments are
 * null, false otherwise.
 */
case class Like(left: Expression, right: Expression, escapeChar: Char = '\\') extends Binary(left, right) {
  override def dataType: DataType = BooleanType
}

/** str rlike regexp - Returns true if `str` matches `regexp`, or false otherwise. */
case class RLike(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = BooleanType
}