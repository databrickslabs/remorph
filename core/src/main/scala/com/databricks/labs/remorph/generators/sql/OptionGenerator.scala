package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{intermediate => ir}

class OptionGenerator(expr: ExpressionGenerator) {

  def generateOption(option: ir.GenericOption): SQL =
    option match {
      case ir.OptionExpression(id, value, supplement) =>
        code"$id = ${expr.generate(value)} ${supplement.map(s => s" $s").getOrElse("")}"
      case ir.OptionString(id, value) =>
        code"$id = '$value'"
      case ir.OptionOn(id) =>
        code"$id = ON"
      case ir.OptionOff(id) =>
        code"$id = OFF"
      case ir.OptionAuto(id) =>
        code"$id = AUTO"
      case ir.OptionDefault(id) =>
        code"$id = DEFAULT"
      case ir.OptionUnresolved(text) =>
        code"$text"
    }

  def generateOptionList(options: Seq[ir.GenericOption]): String =
    options.map(generateOption(_)).mkString(", ")

}
