package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}

class SnowflakeCommandBuilder
    extends SnowflakeParserBaseVisitor[ir.Command]
    with ParserCommon[ir.Command]
    with IncompleteParser[ir.Command] {

  private val expressionBuilder = new SnowflakeExpressionBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedCommand =
    ir.UnresolvedCommand(unparsedInput)

  override def visitDeclareWithDefault(ctx: DeclareWithDefaultContext): ir.Command = {
    val variableName = ctx.id().getText
    val dataType = DataTypeBuilder.buildDataType(ctx.dataType())
    val variableValue = ctx.expr().accept(expressionBuilder)
    ir.CreateVariable(variableName, dataType, Some(variableValue), replace = false)
  }

  override def visitDeclareSimple(ctx: DeclareSimpleContext): ir.Command = {
    val variableName = ctx.id().getText
    val dataType = DataTypeBuilder.buildDataType(ctx.dataType())
    ir.CreateVariable(variableName, dataType, None, replace = false)
  }

  override def visitLetVariableAssignment(ctx: LetVariableAssignmentContext): ir.Command = {
    val variableName = ctx.id().getText
    val variableDataType = Option(ctx.dataType()).flatMap(dt => Some(DataTypeBuilder.buildDataType(dt)))
    val variableValue = ctx.expr().accept(expressionBuilder)

    ir.SetVariable(variableName, variableDataType, variableValue)
  }

}
