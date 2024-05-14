package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ErrorCollector, ParserTestCommon, ProductionErrorCollector}
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}
import org.scalatest.Assertions

trait TSqlParserTestCommon extends ParserTestCommon[TSqlParser] { self: Assertions =>

  override final protected def makeLexer(chars: CharStream): TokenSource = new TSqlLexer(chars)

  override protected def makeErrHandler(chars: String): ErrorCollector =
    new ProductionErrorCollector(chars, "-- test string --")

  override final protected def makeParser(tokenStream: TokenStream): TSqlParser =
    new TSqlParser(tokenStream)
}
