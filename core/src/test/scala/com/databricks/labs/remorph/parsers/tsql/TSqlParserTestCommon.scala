package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.ParserTestCommon
import org.scalatest.Assertions
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}

trait TSqlParserTestCommon extends ParserTestCommon[TSqlParser] { self: Assertions =>

  override final protected def makeLexer(chars: CharStream): TokenSource = new TSqlLexer(chars)

  override final protected def makeParser(tokenStream: TokenStream): TSqlParser = new TSqlParser(tokenStream)
}
