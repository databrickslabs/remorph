package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.GenericOptionContext
import com.databricks.labs.remorph.{intermediate => ir}

class OptionBuilder(vc: TSqlVisitorCoordinator) {

  private[tsql] def buildOptionList(opts: Seq[GenericOptionContext]): ir.OptionLists = {
    val options = opts.map(this.buildOption)
    val (stringOptions, boolFlags, autoFlags, exprValues) = options.foldLeft(
      (Map.empty[String, String], Map.empty[String, Boolean], List.empty[String], Map.empty[String, ir.Expression])) {
      case ((stringOptions, boolFlags, autoFlags, values), option) =>
        option match {
          case ir.OptionString(key, value) =>
            (stringOptions + (key -> value.stripPrefix("'").stripSuffix("'")), boolFlags, autoFlags, values)
          case ir.OptionOn(id) => (stringOptions, boolFlags + (id -> true), autoFlags, values)
          case ir.OptionOff(id) => (stringOptions, boolFlags + (id -> false), autoFlags, values)
          case ir.OptionAuto(id) => (stringOptions, boolFlags, id :: autoFlags, values)
          case ir.OptionExpression(id, expr, _) => (stringOptions, boolFlags, autoFlags, values + (id -> expr))
          case _ => (stringOptions, boolFlags, autoFlags, values)
        }
    }
    new ir.OptionLists(exprValues, stringOptions, boolFlags, autoFlags)
  }

  private[tsql] def buildOption(ctx: TSqlParser.GenericOptionContext): ir.GenericOption = {
    val id = ctx.id(0).getText.toUpperCase()
    ctx match {
      case c if c.DEFAULT() != null => ir.OptionDefault(id)
      case c if c.ON() != null => ir.OptionOn(id)
      case c if c.OFF() != null => ir.OptionOff(id)
      case c if c.AUTO() != null => ir.OptionAuto(id)
      case c if c.STRING() != null => ir.OptionString(id, c.STRING().getText)

      // FOR cannot be allowed as an id as it clashes with the FOR clause in SELECT et al. So
      // we special case it here and elide the FOR. It handles just a few things such as OPTIMIZE FOR UNKNOWN,
      // which becomes "OPTIMIZE", Id(UNKNOWN)
      case c if c.FOR() != null => ir.OptionExpression(id, vc.expressionBuilder.buildId(c.id(1)), None)
      case c if c.expression() != null =>
        val supplement = if (c.id(1) != null) Some(ctx.id(1).getText) else None
        ir.OptionExpression(id, c.expression().accept(vc.expressionBuilder), supplement)
      case _ if id == "DEFAULT" => ir.OptionDefault(id)
      case _ if id == "ON" => ir.OptionOn(id)
      case _ if id == "OFF" => ir.OptionOff(id)
      case _ if id == "AUTO" => ir.OptionAuto(id)
      // All other cases being OptionOn as it is a single keyword representing true
      case _ => ir.OptionOn(id)
    }
  }
}
