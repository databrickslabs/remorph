package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.ParserTestCommon
import org.antlr.v4.runtime.{CharStream, TokenSource, TokenStream}
import org.scalatest.Assertions

trait SnowflakeParserTestCommon extends ParserTestCommon[SnowflakeParser] { self: Assertions =>

  override final protected def makeLexer(chars: CharStream): TokenSource = new SnowflakeLexer(chars)

  override final protected def makeParser(tokenStream: TokenStream): SnowflakeParser = new SnowflakeParser(tokenStream)

}
