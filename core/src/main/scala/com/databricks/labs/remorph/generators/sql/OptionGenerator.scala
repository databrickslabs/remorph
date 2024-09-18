package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.intermediate.{GenericOption, OptionAuto, OptionDefault, OptionExpression, OptionOff, OptionOn, OptionString, OptionUnresolved}

class OptionGenerator(expr: ExpressionGenerator) {

  def generateOption(ctx: GeneratorContext, option: GenericOption): String =
    option match {
      case OptionExpression(id, value, supplement) =>
        s"$id = ${expr.generate(ctx, value)}" + supplement.map(s => s" $s").getOrElse("")
      case OptionString(id, value) =>
        s"$id = '$value'"
      case OptionOn(id) =>
        s"$id = ON"
      case OptionOff(id) =>
        s"$id = OFF"
      case OptionAuto(id) =>
        s"$id = AUTO"
      case OptionDefault(id) =>
        s"$id = DEFAULT"
      case OptionUnresolved(text) =>
        s"$text"
    }

  def generateOptionList(ctx: GeneratorContext, options: Seq[GenericOption]): String =
    options.map(generateOption(ctx, _)).mkString(", ")

}
