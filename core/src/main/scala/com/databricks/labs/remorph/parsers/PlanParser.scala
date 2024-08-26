package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.intermediate.LogicalPlan
import org.antlr.v4.runtime.{CharStream, CharStreams, CommonTokenStream, Parser, TokenSource, TokenStream}

trait PlanParser[P <: Parser] {
  protected def createPlan(parser: P): LogicalPlan
  protected def createParser(stream: TokenStream): P
  protected def createLexer(input: CharStream): TokenSource
  def parse(input: String): LogicalPlan = {
    val inputString = CharStreams.fromString(input)
    val tokenStream = new CommonTokenStream(createLexer(inputString))
    val parser = createParser(tokenStream)
    val errHandler = new ProductionErrorCollector(input, "-- test string --")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    createPlan(parser)
  }
}
