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
