package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.{intermediate => ir}

sealed trait OptionValue
case class OptionList(options: List[GenericOption]) extends OptionValue
case class OptionExpression(expression: ir.Expression, supplement: String) extends OptionValue
case object OptionOn extends OptionValue
case object OptionOff extends OptionValue
case object OptionAuto extends OptionValue
case object OptionDefault extends OptionValue

case class GenericOption(id: String, value: Option[OptionValue])
