package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ErrorCollector, ParserTestCommon, ProductionErrorCollector}
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}
import org.scalatest.Assertions

trait TSqlParserTestCommon extends ParserTestCommon[TSqlParser] { self: Assertions =>

  val vc: TSqlVisitorCoordinator = new TSqlVisitorCoordinator
  override final protected def makeLexer(chars: CharStream): TokenSource = new TSqlLexer(chars)

  override final protected def makeErrStrategy(): TSqlErrorStrategy = new TSqlErrorStrategy

  override protected def makeErrListener(chars: String): ErrorCollector =
    new ProductionErrorCollector(chars, "-- test string --")

  override final protected def makeParser(tokenStream: TokenStream): TSqlParser = {
    val parser = new TSqlParser(tokenStream)
    parser
  }
}
