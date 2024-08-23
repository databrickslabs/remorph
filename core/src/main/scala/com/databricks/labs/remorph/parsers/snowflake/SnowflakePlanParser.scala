package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.intermediate.LogicalPlan
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}

class SnowflakePlanParser extends PlanParser[SnowflakeParser] {
  private val astBuilder = new SnowflakeAstBuilder
  override protected def createLexer(input: CharStream): TokenSource = new SnowflakeLexer(input)
  override protected def createParser(stream: TokenStream): SnowflakeParser = new SnowflakeParser(stream)
  override protected def createPlan(parser: SnowflakeParser): LogicalPlan = {
    val tree = parser.snowflakeFile()
    astBuilder.visit(tree)
  }
}
