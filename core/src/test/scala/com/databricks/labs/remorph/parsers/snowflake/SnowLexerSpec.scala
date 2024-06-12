package com.databricks.labs.remorph.parsers.snowflake

import org.antlr.v4.runtime.{CharStreams, Token}
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.wordspec.AnyWordSpec

class SnowLexerSpec extends AnyWordSpec with Matchers with TableDrivenPropertyChecks {

  private val lexer = new SnowflakeLexer(null)

  "Snowflake Lexer" should {
    "parse string literals" in {

      val testInput = Table(
        ("input", "expected"), // Headers
        (""""quoted""id""", SnowflakeLexer.DOUBLE_QUOTE_ID),
        ("\"quote\"\"andunquote\"\"\"", SnowflakeLexer.DOUBLE_QUOTE_ID),
        ("'hello'", SnowflakeLexer.STRING))

      forAll(testInput) { (input: String, expected: Int) =>
        val inputString = CharStreams.fromString(input)

        lexer.setInputStream(inputString)
        val tok: Token = lexer.nextToken()
        tok.getType should be(expected)
      }
    }

  }

}
