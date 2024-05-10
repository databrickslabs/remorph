package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ErrorCollector, ParserTestCommon}
import org.scalatest.Assertions
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}

trait TSqlParserTestCommon extends ParserTestCommon[TSqlParser] { self: Assertions =>

  override final protected def makeLexer(chars: CharStream): TokenSource = new TSqlLexer(chars)

  override protected def makeErrHandler(chars: String): ErrorCollector = new ErrorCollector(chars, "-- test string --")

  override final protected def makeParser(tokenStream: TokenStream): TSqlParser = {
    val parser = new TSqlParser(tokenStream)
    parser
  }
}
