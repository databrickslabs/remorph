package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.{intermediate => ir}

class ConvertFractionalSecond extends ir.Rule[ir.LogicalPlan] {

  // Please read the note here : https://docs.snowflake.com/en/sql-reference/functions/current_timestamp#arguments
  // TODO Fractional seconds are only displayed if they have been explicitly
  // set in the TIME_OUTPUT_FORMAT parameter for the session (e.g. 'HH24:MI:SS.FF').

  private val timeMapping: Map[Int, String] = Map(
    0 -> "HH:mm:ss",
    1 -> "HH:mm:ss",
    2 -> "HH:mm:ss",
    3 -> "HH:mm:ss",
    4 -> "HH:mm:ss",
    5 -> "HH:mm:ss",
    6 -> "HH:mm:ss",
    7 -> "HH:mm:ss",
    8 -> "HH:mm:ss",
    9 -> "HH:mm:ss")

  override def apply(plan: ir.LogicalPlan): ir.LogicalPlan = {
    plan transformAllExpressions {
      case ir.CallFunction("CURRENT_TIME", right) => handleSpecialTSFunctions("CURRENT_TIME", right)
      case ir.CallFunction("LOCALTIME", right) => handleSpecialTSFunctions("LOCALTIME", right)
      case ir.CallFunction("CURRENT_TIMESTAMP", right) =>
        if (right.isEmpty) {
          ir.CurrentTimestamp()
        } else {
          handleSpecialTSFunctions("CURRENT_TIMESTAMP", right)
        }
      case ir.CallFunction("LOCALTIMESTAMP", right) =>
        if (right.isEmpty) {
          ir.CurrentTimestamp()
        } else {
          handleSpecialTSFunctions("LOCALTIMESTAMP", right)
        }
    }
  }

  private def getIntegerValue(literal: Option[ir.Literal]): Option[Int] = literal match {
    case Some(ir.Literal(value: Int, _)) => Some(value)
    case _ => None
  }

  private def handleSpecialTSFunctions(functionName: String, arguments: Seq[ir.Expression]): ir.Expression = {
    val timeFormat = timeMapping(getIntegerValue(arguments.headOption.flatMap {
      case lit: ir.Literal => Some(lit)
      case _ => None
    }).getOrElse(0))

    // https://docs.snowflake.com/en/sql-reference/functions/current_timestamp
    // https://docs.snowflake.com/en/sql-reference/functions/current_time
    // https://docs.snowflake.com/en/sql-reference/functions/localtimestamp
    val formatString = functionName match {
      case "CURRENT_TIME" | "LOCALTIME" => timeFormat
      case _ => s"yyyy-MM-dd $timeFormat.SSS"
    }
    ir.DateFormatClass(ir.CurrentTimestamp(), ir.Literal(formatString))
  }

}
