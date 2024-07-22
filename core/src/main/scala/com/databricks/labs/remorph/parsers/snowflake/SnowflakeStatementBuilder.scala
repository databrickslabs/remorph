package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.Statement
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.LetContext
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}

class SnowflakeStatementBuilder
    extends SnowflakeParserBaseVisitor[ir.Statement]
    with ParserCommon[ir.Statement]
    with IncompleteParser[ir.Statement] {

  private val expressionBuilder = new SnowflakeExpressionBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedStatement =
    ir.UnresolvedStatement(unparsedInput)

  override def visitDeclareStatement(ctx: SnowflakeParser.DeclareStatementContext): Statement = {
    val variableName = ctx.id().getText
    val variableDataType = Some(DataTypeBuilder.buildDataType(ctx.dataType()))
    val variableValue = None
    ir.SetVariable(variableName, variableDataType, variableValue)
  }

  override def visitLet(ctx: LetContext): ir.Statement = {
    val variableName = ctx.id().getText
    val variableDataType = Option(ctx.dataType()).flatMap(dt => Some(DataTypeBuilder.buildDataType(dt)))

    ir.SetVariable(variableName, variableDataType, Some(ctx.expr().accept(expressionBuilder)))

  }

}
