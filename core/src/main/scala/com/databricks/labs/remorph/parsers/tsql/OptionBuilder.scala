package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers._
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.GenericOptionContext

class OptionBuilder(expressionBuilder: TSqlExpressionBuilder) {

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
    ctx match {
      case c if c.DEFAULT() != null => OptionDefault(id)
      case c if c.ON() != null => OptionOn(id)
      case c if c.OFF() != null => OptionOff(id)
      case c if c.AUTO() != null => OptionAuto(id)
      case c if c.STRING() != null => OptionString(id, c.STRING().getText)

      // FOR cannot be allowed as an id as it clashes with the FOR clause in SELECT et al. So
      // we special case it here and elide the FOR. It handles just a few things such as OPTIMIZE FOR UNKNOWN,
      // which becomes "OPTIMIZE", Id(UNKNOWN)
      case c if c.FOR() != null => OptionExpression(id, expressionBuilder.visitId(c.id(1)), None)
      case c if c.expression() != null =>
        val supplement = if (c.id(1) != null) Some(ctx.id(1).getText) else None
        OptionExpression(id, c.expression().accept(expressionBuilder), supplement)
      case _ if id == "DEFAULT" => OptionDefault(id)
      case _ if id == "ON" => OptionOn(id)
      case _ if id == "OFF" => OptionOff(id)
      case _ if id == "AUTO" => OptionAuto(id)
      // All other cases being OptionOn as it is a single keyword representing true
      case _ => OptionOn(id)
    }
  }
}
