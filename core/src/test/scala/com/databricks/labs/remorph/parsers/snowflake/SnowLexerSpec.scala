package com.databricks.labs.remorph.parsers.snowflake

import org.antlr.v4.runtime.{CharStreams, Token}
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.wordspec.AnyWordSpec

class SnowLexerSpec extends AnyWordSpec with Matchers with TableDrivenPropertyChecks {

  private val lexer = new SnowflakeLexer(null)

  // TODO: Expand this test to cover all token types, and maybe all tokens
  "Snowflake Lexer" should {
    "parse string literals and ids" in {

      val testInput = Table(
        ("child", "expected"), // Headers

        ("'And it''s raining'", SnowflakeLexer.STRING),
        ("""'Tab\oir'""", SnowflakeLexer.STRING),
        ("""'Tab\'oir'""", SnowflakeLexer.STRING),
        ("'hello'", SnowflakeLexer.STRING),
        (""""quoted""id"""", SnowflakeLexer.DOUBLE_QUOTE_ID),
        ("\"quote\"\"andunquote\"\"\"", SnowflakeLexer.DOUBLE_QUOTE_ID))

      forAll(testInput) { (input: String, expectedType: Int) =>
        val inputString = CharStreams.fromString(input)

        lexer.setInputStream(inputString)
        val tok: Token = lexer.nextToken()
        tok.getType shouldBe expectedType
        tok.getText shouldBe input
      }
    }

  }

}
