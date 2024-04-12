package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

case class Column(name: String) extends Expression with AstExtension {}

abstract class Predicate extends Expression with AstExtension {}

case class And(left: Predicate, right: Predicate) extends Predicate {}
case class Or(left: Predicate, right: Predicate) extends Predicate {}
case class Not(pred: Predicate) extends Predicate {}

case class Equals(left: Expression, right: Expression) extends Predicate {}
case class NotEquals(left: Expression, right: Expression) extends Predicate {}
case class GreaterThan(left: Expression, right: Expression) extends Predicate {}
case class LesserThan(left: Expression, right: Expression) extends Predicate {}
case class GreaterThanOrEqual(left: Expression, right: Expression) extends Predicate {}
case class LesserThanOrEqual(left: Expression, right: Expression) extends Predicate {}

