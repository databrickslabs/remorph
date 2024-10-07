package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon}
import com.databricks.labs.remorph.{intermediate => ir}

class SnowflakeCommandBuilder
    extends SnowflakeParserBaseVisitor[ir.Command]
    with ParserCommon[ir.Command]
    with IncompleteParser[ir.Command] {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val typeBuilder = new SnowflakeTypeBuilder

  protected override def wrapUnresolvedInput(unparsedInput: RuleNode): ir.UnresolvedCommand =
    ir.UnresolvedCommand(getTextFromParserRuleContext(unparsedInput.getRuleContext))

  // This gets called when a visitor is not implemented so the default visitChildren is called, and it returns more
  // than one result. This is a sign that the visitor is not implemented and we need to at least implement a placeholder
  // visitor
  override protected def aggregateResult(aggregate: ir.Command, nextResult: ir.Command): ir.Command = {
    // scalastyle:off
    println("WARNING: Aggregating ir.Command results because of unimplemented visitor(s).")
    // scalastyle:on
    // Note that here we are just returning one of the nodes, which avoids returning null so long as they are not BOTH
    // null. This not correct, but it is a placeholder until we implement the missing visitor, so that we get a warning.
    if (nextResult == null) {
      aggregate
    } else {
      nextResult
    }
  }

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
