package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{FunctionBuilder, FunctionDefinition, StringConverter}
import com.databricks.labs.remorph.{intermediate => ir}

class TSqlFunctionBuilder extends FunctionBuilder with StringConverter {

  private val tSqlFunctionDefinitionPf: PartialFunction[String, FunctionDefinition] = {
    case """$PARTITION""" => FunctionDefinition.notConvertible(0)
    case "@@CURSOR_ROWS" => FunctionDefinition.notConvertible(0)
    case "@@DBTS" => FunctionDefinition.notConvertible(0)
    case "@@FETCH_STATUS" => FunctionDefinition.notConvertible(0)
    case "@@LANGID" => FunctionDefinition.notConvertible(0)
    case "@@LANGUAGE" => FunctionDefinition.notConvertible(0)
    case "@@LOCKTIMEOUT" => FunctionDefinition.notConvertible(0)
    case "@@MAX_CONNECTIONS" => FunctionDefinition.notConvertible(0)
    case "@@MAX_PRECISION" => FunctionDefinition.notConvertible(0)
    case "@@NESTLEVEL" => FunctionDefinition.notConvertible(0)
    case "@@OPTIONS" => FunctionDefinition.notConvertible(0)
    case "@@REMSERVER" => FunctionDefinition.notConvertible(0)
    case "@@SERVERNAME" => FunctionDefinition.notConvertible(0)
    case "@@SERVICENAME" => FunctionDefinition.notConvertible(0)
    case "@@SPID" => FunctionDefinition.notConvertible(0)
    case "@@TEXTSIZE" => FunctionDefinition.notConvertible(0)
    case "@@VERSION" => FunctionDefinition.notConvertible(0)
    case "COLLATIONPROPERTY" => FunctionDefinition.notConvertible(2)
    case "CONTAINSTABLE" => FunctionDefinition.notConvertible(0)
    case "CUBE" => FunctionDefinition.standard(1, Int.MaxValue) // Snowflake hard codes this
    case "FREETEXTTABLE" => FunctionDefinition.notConvertible(0)
    case "GET_BIT" => FunctionDefinition.standard(2).withConversionStrategy(rename)
    case "HIERARCHYID" => FunctionDefinition.notConvertible(0)
    case "ISNULL" => FunctionDefinition.standard(2).withConversionStrategy(rename)
    case "LEFT_SHIFT" => FunctionDefinition.standard(2).withConversionStrategy(rename)
    case "MODIFY" => FunctionDefinition.xml(1)
    case "NEXTVALUEFOR" => FunctionDefinition.standard(1).withConversionStrategy(nextValueFor)
    case "RIGHT_SHIFT" => FunctionDefinition.standard(2).withConversionStrategy(rename)
    case "ROLLUP" => FunctionDefinition.standard(1, Int.MaxValue) // Snowflake hard codes this
    case "SEMANTICKEYPHRASETABLE" => FunctionDefinition.notConvertible(0)
    case "SEMANTICSIMILARITYDETAILSTABLE" => FunctionDefinition.notConvertible(0)
    case "SEMANTICSSIMILARITYTABLE" => FunctionDefinition.notConvertible(0)
    case "SET_BIT" => FunctionDefinition.standard(2, 3).withConversionStrategy(rename)
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
      case "GET_BIT" => ir.CallFunction(convertString(irName, "GETBIT"), args)
      case "LEFT_SHIFT" => ir.CallFunction(convertString(irName, "LEFTSHIFT"), args)
      case "RIGHT_SHIFT" => ir.CallFunction(convertString(irName, "RIGHTSHIFT"), args)
      case _ => ir.CallFunction(irName, args)
    }
  }

}
