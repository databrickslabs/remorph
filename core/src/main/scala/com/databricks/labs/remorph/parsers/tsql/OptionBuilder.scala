package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers._
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.GenericOptionContext

class OptionBuilder {

  private val expressionBuilder = new TSqlExpressionBuilder

  private[tsql] def buildOptionList(opts: Seq[GenericOptionContext]): OptionLists = {
    val options = opts.map(this.buildOption)
    val (stringOptions, boolFlags, autoFlags, exprValues) = options.foldLeft(
      (Map.empty[String, String], Map.empty[String, Boolean], List.empty[String], Map.empty[String, ir.Expression])) {
      case ((stringOptions, boolFlags, autoFlags, values), option) =>
        option match {
          case OptionString(key, value) =>
            (stringOptions + (key -> value.stripPrefix("'").stripSuffix("'")), boolFlags, autoFlags, values)
          case OptionOn(id) => (stringOptions, boolFlags + (id -> true), autoFlags, values)
          case OptionOff(id) => (stringOptions, boolFlags + (id -> false), autoFlags, values)
          case OptionAuto(id) => (stringOptions, boolFlags, id :: autoFlags, values)
          case OptionExpression(id, expr, _) => (stringOptions, boolFlags, autoFlags, values + (id -> expr))
          case _ => (stringOptions, boolFlags, autoFlags, values)
        }
    }
    new OptionLists(exprValues, stringOptions, boolFlags, autoFlags)
  }

  private[tsql] def buildOption(ctx: TSqlParser.GenericOptionContext): GenericOption = {
    val id = ctx.id(0).getText.toUpperCase()
    id match {
      case "DEFAULT" => OptionDefault(id)
      case "ON" => OptionOn(id)
      case "OFF" => OptionOff(id)
      case "AUTO" => OptionAuto(id)
      case _ if ctx.DEFAULT() != null => OptionDefault(id)
      case _ if ctx.ON() != null => OptionOn(id)
      case _ if ctx.OFF() != null => OptionOff(id)
      case _ if ctx.AUTO() != null => OptionAuto(id)
      case _ if ctx.STRING() != null => OptionString(id, ctx.STRING().getText)
      case _ if ctx.expression() != null =>
        val supplement = if (ctx.id(1) != null) Some(ctx.id(1).getText) else None
        OptionExpression(id, ctx.expression().accept(expressionBuilder), supplement)

      // All other cases being OptionOn as it is a single keyword representing true
      case _ => OptionOn(id)
    }
  }
}
