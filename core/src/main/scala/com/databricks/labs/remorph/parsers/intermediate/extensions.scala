package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

case class Column(name: String) extends Expression with AstExtension {}

abstract class Unary(pred: Expression) extends Expression {}
abstract class Binary(left: Expression, right: Expression) extends Expression {}

trait Predicate extends Expression with AstExtension

case class And(left: Predicate, right: Predicate) extends Binary(left, right) with Predicate {}
case class Or(left: Predicate, right: Predicate) extends Binary(left, right) with Predicate {}
case class Not(pred: Predicate) extends Unary(pred) with Predicate {}

case class Equals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class NotEquals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
