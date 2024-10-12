package com.databricks.labs.remorph.parsers
import com.databricks.labs.remorph.{intermediate => ir}

import java.util.Locale

trait ConversionStrategy {
  def convert(irName: String, args: Seq[ir.Expression]): ir.Expression
}

trait StringConverter {
  // Preserves case if the original name was all lower case. Otherwise, converts to upper case.
  // All bets are off if the original name was mixed case, but that is rarely seen in SQL and we are
  // just making reasonable efforts here.
  def convertString(irName: String, newName: String): String = {
    if (irName.forall(c => c.isLower || c == '_')) newName.toLowerCase(Locale.ROOT) else newName
  }
}
