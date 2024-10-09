package com.databricks.labs.remorph.intermediate

trait GenericOption {
  def id: String
}

case class OptionExpression(id: String, value: Expression, supplement: Option[String]) extends GenericOption
case class OptionString(id: String, value: String) extends GenericOption
case class OptionOn(id: String) extends GenericOption
case class OptionOff(id: String) extends GenericOption
case class OptionAuto(id: String) extends GenericOption
case class OptionDefault(id: String) extends GenericOption
case class OptionUnresolved(id: String) extends GenericOption

class OptionLists(
    val expressionOpts: Map[String, Expression],
    val stringOpts: Map[String, String],
    val boolFlags: Map[String, Boolean],
    val autoFlags: List[String]) {}
