package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{intermediate => ir}

class OptionGenerator(expr: ExpressionGenerator) {

  def generateOption(ctx: GeneratorContext, option: ir.GenericOption): SQL =
    option match {
      case ir.OptionExpression(id, value, supplement) =>
        tba"$id = ${expr.generate(ctx, value)} ${supplement.map(s => s" $s").getOrElse("")}"
      case ir.OptionString(id, value) =>
        tba"$id = '$value'"
      case ir.OptionOn(id) =>
        tba"$id = ON"
      case ir.OptionOff(id) =>
        tba"$id = OFF"
      case ir.OptionAuto(id) =>
        tba"$id = AUTO"
      case ir.OptionDefault(id) =>
        tba"$id = DEFAULT"
      case ir.OptionUnresolved(text) =>
        tba"$text"
    }

  def generateOptionList(ctx: GeneratorContext, options: Seq[ir.GenericOption]): String =
    options.map(generateOption(ctx, _)).mkString(", ")

}
