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

  // TODO: Implement Cursor and Exception for Declare Statements.
  // TODO: Implement Cursor for Let Statements.

  override def visitDeclareWithDefault(ctx: DeclareWithDefaultContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val dataType = DataTypeBuilder.buildDataType(ctx.dataType())
    val variableValue = ctx.expr().accept(expressionBuilder)
    ir.CreateVariable(variableName, dataType, Some(variableValue), replace = false)
  }

  override def visitDeclareSimple(ctx: DeclareSimpleContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val dataType = DataTypeBuilder.buildDataType(ctx.dataType())
    ir.CreateVariable(variableName, dataType, None, replace = false)
  }

  override def visitDeclareResultSet(ctx: DeclareResultSetContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val dataType = ir.StructType()
    val variableValue = ctx.expr() match {
      case null => None
      case stmt => Some(stmt.accept(expressionBuilder))
    }

    ir.CreateVariable(variableName, dataType, variableValue, replace = false)
  }

  override def visitLetVariableAssignment(ctx: LetVariableAssignmentContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val variableValue = ctx.expr().accept(expressionBuilder)

    val variableDataType = variableValue match {
      case _: ir.ScalarSubquery => Some(ir.StructType())
      case _ => Option(ctx.dataType()).flatMap(dt => Some(DataTypeBuilder.buildDataType(dt)))
    }

    ir.SetVariable(variableName, variableValue, variableDataType)
  }

  override  def visitSnowSqlCommand(ctx: SnowSqlCommandContext): ir.UnresolvedCommand = {
    ir.UnresolvedCommand(ctx.getText)
  }

}
