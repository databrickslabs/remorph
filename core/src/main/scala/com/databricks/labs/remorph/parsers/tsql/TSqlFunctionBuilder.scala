package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ConversionStrategy, FunctionBuilder, FunctionDefinition, intermediate => ir}

class TSqlFunctionBuilder extends FunctionBuilder {

  private val tSqlFunctionDefinitionPf: PartialFunction[String, FunctionDefinition] = {
    case "@@CURSOR_STATUS" => FunctionDefinition.notConvertible(0)
    case "@@FETCH_STATUS" => FunctionDefinition.notConvertible(0)
    // The ConversionStrategy is used to rename ISNULL to IFNULL
    case "ISNULL" => FunctionDefinition.standard(2).withConversionStrategy(TSqlFunctionConverters.FunctionRename)
    case "MODIFY" => FunctionDefinition.xml(1)
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
}

// Note that these are left as objects, though we will possibly have a class per function in the future
object TSqlFunctionConverters {

  object FunctionRename extends ConversionStrategy {
    override def convert(irName: String, args: Seq[ir.Expression]): ir.Expression = {
      irName.toUpperCase() match {
        case "ISNULL" => ir.CallFunction(convertString(irName, "IFNULL"), args)
        case _ => ir.CallFunction(irName, args)
      }
    }
  }

}
