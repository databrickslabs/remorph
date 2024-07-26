package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.LetContext
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}

class SnowflakeCommandBuilder
    extends SnowflakeParserBaseVisitor[ir.Command]
    with ParserCommon[ir.Command]
    with IncompleteParser[ir.Command] {

  private val expressionBuilder = new SnowflakeExpressionBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedCommand =
    ir.UnresolvedCommand(unparsedInput)

  override def visitLet(ctx: LetContext): ir.Command = {
    val variableName = ctx.id().getText
    val variableDataType = Option(ctx.dataType()).flatMap(dt => Some(DataTypeBuilder.buildDataType(dt)))
    val variableValue = ctx.expr().accept(expressionBuilder)

    ir.SetVariable(variableName, ir.ExpressionLogicalPlan(variableValue))
  }

}
