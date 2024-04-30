package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

case class Column(name: String) extends Expression with AstExtension {}

abstract class Unary(pred: Expression) extends Expression {}
abstract class Binary(left: Expression, right: Expression) extends Expression {}

trait Predicate extends AstExtension

case class And(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class Or(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class Not(pred: Expression) extends Unary(pred) with Predicate {}

case class Equals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class NotEquals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}

case class Count(expression: Expression) extends Expression {}
case class Sum(expression: Expression) extends Expression {}
case class Avg(expression: Expression) extends Expression {}
case class Max(expression: Expression) extends Expression {}
case class Min(expression: Expression) extends Expression {}

case object Noop extends Expression
case object RowNumber extends Expression {}
case class NTile(expression: Expression) extends Expression {}

case class WithCTE(ctes: Seq[Relation], query: Relation) extends RelationCommon {}
case class CTEDefinition(tableName: String, columns: Seq[Expression], cte: Relation) extends RelationCommon {}

case class Star(objectName: Option[String]) extends Expression {}

case class WhenBranch(condition: Expression, expression: Expression)
case class Case(expression: Option[Expression], branches: Seq[WhenBranch], otherwise: Option[Expression])
    extends Expression {}

case class Exists(relation: Relation) extends Expression {}

case class IsIn(relation: Relation, expression: Expression) extends Expression {}

case class Like(expression: Expression, patterns: Seq[Expression], escape: Option[Expression], caseSensitive: Boolean)
    extends Expression {}

case class RLike(expression: Expression, pattern: Expression) extends Expression {}

case class IsNull(expression: Expression) extends Expression {}

case class UnresolvedOperator(unparsed_target: String) extends Expression {}

// TODO: TSQL grammar has a number of operators not yet supported - add them here, if not already supported

// Arithmetic expressions
case class Multiply(left: Expression, right: Expression) extends Binary(left, right) {}
case class Divide(left: Expression, right: Expression) extends Binary(left, right) {}
case class Mod(left: Expression, right: Expression) extends Binary(left, right) {}
case class Add(left: Expression, right: Expression) extends Binary(left, right) {}
case class Subtract(left: Expression, right: Expression) extends Binary(left, right) {}

// Binary bitwise expressions
case class BitwiseAnd(left: Expression, right: Expression) extends Binary(left, right) {}
case class BitwiseOr(left: Expression, right: Expression) extends Binary(left, right) {}
case class BitwiseXor(left: Expression, right: Expression) extends Binary(left, right) {}

// Other binary expressions
case class Concat(left: Expression, right: Expression) extends Binary(left, right) {}

// Some statements, such as SELECT, do not require a table specification
case class NoTable() extends Relation {}

case class Batch(statements: Seq[Plan]) extends Plan
