package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.{intermediate => ir}

class SnowflakeCommandBuilder extends SnowflakeParserBaseVisitor[ir.Command] with ParserCommon[ir.Command] {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val typeBuilder = new SnowflakeTypeBuilder

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(msg: String): ir.Command = {
    ir.UnresolvedCommand(msg)
  }

  // Concrete visitors

  // TODO: Implement Cursor and Exception for Declare Statements.
  // TODO: Implement Cursor for Let Statements.

  override def visitDeclareWithDefault(ctx: DeclareWithDefaultContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val dataType = typeBuilder.buildDataType(ctx.dataType())
    val variableValue = ctx.expr().accept(expressionBuilder)
    ir.CreateVariable(variableName, dataType, Some(variableValue), replace = false)
  }

  override def visitDeclareSimple(ctx: DeclareSimpleContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val dataType = typeBuilder.buildDataType(ctx.dataType())
    ir.CreateVariable(variableName, dataType, None, replace = false)
  }

  override def visitDeclareResultSet(ctx: DeclareResultSetContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val variableValue = ctx.expr() match {
      case null => None
      case stmt => Some(stmt.accept(expressionBuilder))
    }
    val dataType = ir.StructType(Seq())
    ir.CreateVariable(variableName, dataType, variableValue, replace = false)
  }

  override def visitLetVariableAssignment(ctx: LetVariableAssignmentContext): ir.Command = {
    val variableName = ctx.id().accept(expressionBuilder).asInstanceOf[ir.Id]
    val variableValue = ctx.expr().accept(expressionBuilder)

    val variableDataType = variableValue match {
      case s: ir.ScalarSubquery => Some(s.dataType)
      case _ => Option(ctx.dataType()).flatMap(dt => Some(typeBuilder.buildDataType(dt)))
    }

    ir.SetVariable(variableName, variableValue, variableDataType)
  }

  override def visitExecuteTask(ctx: ExecuteTaskContext): ir.Command = {
    ir.UnresolvedCommand(getTextFromParserRuleContext(ctx))
  }
}
