package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{Result, intermediate => ir}

class OptionGenerator(expr: ExpressionGenerator) {

  def generateOption(ctx: GeneratorContext, option: ir.GenericOption): Result[String] =
    option match {
      case ir.OptionExpression(id, value, supplement) =>
        sql"$id = ${expr.generate(ctx, value)} ${supplement.map(s => s" $s").getOrElse("")}"
      case ir.OptionString(id, value) =>
        sql"$id = '$value'"
      case ir.OptionOn(id) =>
        sql"$id = ON"
      case ir.OptionOff(id) =>
        sql"$id = OFF"
      case ir.OptionAuto(id) =>
        sql"$id = AUTO"
      case ir.OptionDefault(id) =>
        sql"$id = DEFAULT"
      case ir.OptionUnresolved(text) =>
        sql"$text"
    }

  def generateOptionList(ctx: GeneratorContext, options: Seq[ir.GenericOption]): String =
    options.map(generateOption(ctx, _)).mkString(", ")

}
