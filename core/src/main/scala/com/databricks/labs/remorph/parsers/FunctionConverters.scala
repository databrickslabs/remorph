package com.databricks.labs.remorph.parsers
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import java.util.Locale

// A set of functions that convert between different representations of SQL functions, sometimes
// depending on the SQL dialect. They could be one big match statement if all the conversions are trivial renames,
// however, if the conversions are more complex, they can be implemented as separate conversion strategies.

sealed trait ConversionStrategy {
  def convert(irName: String, args: Seq[ir.Expression], dialect: SqlDialect): ir.Expression
}

object FunctionConverters {

  // Preserves case if the original name was all lower case. Otherwise, converts to upper case.
  // All bets are off if the original name was mixed case, but that is rarely seen in SQL and we are
  // just making reasonable efforts here.
  private def convertString(irName: String, newName: String): String = {
    if (irName.forall(_.isLower)) newName.toLowerCase(Locale.ROOT) else newName
  }

  object FunctionRename extends ConversionStrategy {
    override def convert(irName: String, args: Seq[ir.Expression], dialect: SqlDialect): ir.Expression = {
      (irName.toUpperCase(), dialect) match {
        case ("ISNULL", TSql) => ir.CallFunction(FunctionConverters.convertString(irName, "IFNULL"), args)
        case _ => ir.CallFunction(irName, args)
      }
    }
  }
}
