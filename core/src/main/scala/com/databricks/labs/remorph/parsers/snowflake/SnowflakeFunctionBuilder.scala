package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{ConversionStrategy, FunctionBuilder, FunctionDefinition, intermediate => ir}

class SnowflakeFunctionBuilder extends FunctionBuilder {

  private val SnowflakeFunctionDefinitionPf: PartialFunction[String, FunctionDefinition] = {
    case "IFNULL" => FunctionDefinition.standard(2)
    case "ISNULL" => FunctionDefinition.standard(1)
  }

  override def functionDefinition(name: String): Option[FunctionDefinition] =
    // If not found, check common functions
    SnowflakeFunctionDefinitionPf.lift(name.toUpperCase()).orElse(super.functionDefinition(name))

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

object SnowflakeFunctionConverters {

  object FunctionRename extends ConversionStrategy {
    override def convert(irName: String, args: Seq[ir.Expression]): ir.Expression = {
      irName.toUpperCase() match {
        case _ => ir.CallFunction(irName, args)
      }
    }
  }
}
