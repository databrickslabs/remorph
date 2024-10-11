package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{ErrorCollector, ParserTestCommon, ProductionErrorCollector}
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}
import org.scalatest.Assertions

trait SnowflakeParserTestCommon extends ParserTestCommon[SnowflakeParser] { self: Assertions =>

  protected val vc: SnowflakeVisitorCoordinator =
    new SnowflakeVisitorCoordinator(SnowflakeParser.VOCABULARY, SnowflakeParser.ruleNames)
  override final protected def makeLexer(chars: CharStream): TokenSource = new SnowflakeLexer(chars)

  override final protected def makeErrStrategy(): SnowflakeErrorStrategy = new SnowflakeErrorStrategy

  override final protected def makeErrListener(chars: String): ErrorCollector =
    new ProductionErrorCollector(chars, "-- test string --")

  override final protected def makeParser(tokenStream: TokenStream): SnowflakeParser = {
    val parser = new SnowflakeParser(tokenStream)
    parser
  }
}
