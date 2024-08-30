package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.intermediate.LogicalPlan
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}

class TSqlPlanParser extends PlanParser[TSqlParser] {
  private val astBuilder = new TSqlAstBuilder()
  override protected def createPlan(parser: TSqlParser): LogicalPlan = astBuilder.visit(parser.tSqlFile())
  override protected def createParser(stream: TokenStream): TSqlParser = new TSqlParser(stream)
  override protected def createLexer(input: CharStream): TokenSource = new TSqlLexer(input)
}
