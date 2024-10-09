package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{intermediate => ir}

class OptionGenerator(expr: ExpressionGenerator) {

  def generateOption(ctx: GeneratorContext, option: ir.GenericOption): String =
    option match {
      case ir.OptionExpression(id, value, supplement) =>
        s"$id = ${expr.generate(ctx, value)}" + supplement.map(s => s" $s").getOrElse("")
      case ir.OptionString(id, value) =>
        s"$id = '$value'"
      case ir.OptionOn(id) =>
        s"$id = ON"
      case ir.OptionOff(id) =>
        s"$id = OFF"
      case ir.OptionAuto(id) =>
        s"$id = AUTO"
      case ir.OptionDefault(id) =>
        s"$id = DEFAULT"
      case ir.OptionUnresolved(text) =>
        s"$text"
    }

  def generateOptionList(ctx: GeneratorContext, options: Seq[ir.GenericOption]): String =
    options.map(generateOption(ctx, _)).mkString(", ")

}
