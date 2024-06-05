package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{FunctionBuilder, FunctionDefinition, StringConverter, intermediate => ir}

class TSqlFunctionBuilder extends FunctionBuilder with StringConverter {

  private val tSqlFunctionDefinitionPf: PartialFunction[String, FunctionDefinition] = {
    case "@@CURSOR_STATUS" => FunctionDefinition.notConvertible(0)
    case "@@FETCH_STATUS" => FunctionDefinition.notConvertible(0)
    // The ConversionStrategy is used to rename ISNULL to IFNULL
    case "ISNULL" => FunctionDefinition.standard(2).withConversionStrategy(rename)
    case "MODIFY" => FunctionDefinition.xml(1)
    case "NEXTVALUEFOR" => FunctionDefinition.standard(1).withConversionStrategy(nextValueFor)
  }

  override def functionDefinition(name: String): Option[FunctionDefinition] =
    // If not found, check common functions
    tSqlFunctionDefinitionPf.lift(name.toUpperCase()).orElse(super.functionDefinition(name))

  def applyConversionStrategy(
      functionArity: FunctionDefinition,
      args: Seq[ir.Expression],
      irName: String): ir.Expression = {
    functionArity.conversionStrategy match {
      case Some(strategy) => strategy.convert(irName, args)
      case _ => ir.CallFunction(irName, args)
    }
  }

  // TSql specific function converters
  //
  private[tsql] def nextValueFor(irName: String, args: Seq[ir.Expression]): ir.Expression = {
    // Note that this conversion assumes that the CREATE SEQUENCE it references was an increment in ascending order.
    // We may run across instances where this is not the case, and will have to handle that as a special case, perhaps
    // with external procedures or functions in Java/Scala, or even python.
    // For instance a SequenceHandler supplied by the user.
    //
    // Given this, then we use this converter rather than just the simple Rename converter.
    // TODO: Implement external SequenceHandler?
    ir.CallFunction("MONOTONICALLY_INCREASING_ID", List.empty)
  }

  private[tsql] def rename(irName: String, args: Seq[ir.Expression]): ir.Expression = {
    irName.toUpperCase() match {
      case "ISNULL" => ir.CallFunction(convertString(irName, "IFNULL"), args)
      case _ => ir.CallFunction(irName, args)
    }
  }

}
