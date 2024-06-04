package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ConversionStrategy, FunctionBuilder, FunctionDefinition, StringConverter, intermediate => ir}

class TSqlFunctionBuilder extends FunctionBuilder {

  private val tSqlFunctionDefinitionPf: PartialFunction[String, FunctionDefinition] = {
    case "@@CURSOR_STATUS" => FunctionDefinition.notConvertible(0)
    case "@@FETCH_STATUS" => FunctionDefinition.notConvertible(0)
    // The ConversionStrategy is used to rename ISNULL to IFNULL
    case "ISNULL" => FunctionDefinition.standard(2).withConversionStrategy(TSqlFunctionConverters.Rename)
    case "MODIFY" => FunctionDefinition.xml(1)
    case "NEXTVALUEFOR" => FunctionDefinition.standard(1).withConversionStrategy(nextValueFor)
  }
  
  private def nextValueFor(irName: String, args: Seq[ir.Expression]): ir.Expression = {
      // Note that this conversion assumes that the CREATE SEQUENCE it references was an increment in ascending order.
      // We may run across instances where this is not the case, and will have to handle that as a special case, perhaps
      // with external procedures or functions in Java/Scala, or even python.
      // For instance a SequenceHandler supplied by the user.
      //
      // Given this, then we use this converter rather than just the simple Rename converter.
      // TODO: Implement external SequenceHandler?
      ir.CallFunction("MONOTONICALLY_INCREASING_ID", List.empty)
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

// TSQL specific function converters
//
// Note that these are left as objects, though we will possibly have a class per function in the future
// Each function can specify its own ConversionStrategy, and some will need to be very specific,
// hence perhaps moving to a class per function may be a better idea.
object TSqlFunctionConverters {

  object Rename extends ConversionStrategy with StringConverter {
    override def convert(irName: String, args: Seq[ir.Expression]): ir.Expression = {
      irName.toUpperCase() match {
        case "ISNULL" => ir.CallFunction(convertString(irName, "IFNULL"), args)
        case _ => ir.CallFunction(irName, args)
      }
    }
  }

  object NextValueFor extends ConversionStrategy {
    override def convert(irName: String, args: Seq[ir.Expression]): ir.Expression = {
      // Note that this conversion assumes that the CREATE SEQUENCE it references was an increment in ascending order.
      // We may run across instances where this is not the case, and will have to handle that as a special case, perhaps
      // with external procedures or functions in Java/Scala, or even python.
      // For instance a SequenceHandler supplied by the user.
      //
      // Given this, then we use this converter rather than just the simple Rename converter.
      // TODO: Implement external SequenceHandler?
      ir.CallFunction("MONOTONICALLY_INCREASING_ID", List.empty)
    }
  }

  object WindowingFunctions extends ConversionStrategy {
    override def convert(irName: String, args: Seq[ir.Expression]): ir.Expression = irName match {
      // MONOTONICALLY_INCREASING_ID is not a windowing function in Databricks SQL, hence this will
      // not work with OVER clauses. In that case a better translation is
      // ROW_NUMBER() OVER (ORDER BY ...)
      case "MONOTONICALLY_INCREASING_ID" =>
        ir.CallFunction("ROW_NUMBER", args)
      case _ => ir.CallFunction(irName, args)
    }
  }

}
