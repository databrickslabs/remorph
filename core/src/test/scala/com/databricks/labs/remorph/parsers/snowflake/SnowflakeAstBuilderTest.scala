package com.databricks.labs.remorph.parsers.snowflake

import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.scalatest.funsuite.AnyFunSuite

class SnowflakeAstBuilderTest extends AnyFunSuite {
  test("...") {
    val charStream = CharStreams.fromString("TRUE")

    val lexer = new SnowflakeLexer(charStream)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val astBuilder = new SnowflakeAstBuilder()
    val parseTree = parser.true_false()

    val result = astBuilder.typedVisit(parseTree)

    assert(result == 1)
  }
}
