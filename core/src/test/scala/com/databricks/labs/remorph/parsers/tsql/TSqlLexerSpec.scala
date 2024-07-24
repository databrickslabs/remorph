package com.databricks.labs.remorph.parsers.tsql

import org.antlr.v4.runtime.{CharStreams, Token}
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.wordspec.AnyWordSpec

class TSqlLexerSpec extends AnyWordSpec with Matchers with TableDrivenPropertyChecks {

  private val lexer = new TSqlLexer(null)

  // TODO: Expand this test to cover all token types, and maybe all tokens
  "TSqlLexer" should {
    "parse string literals and ids" in {

      val testInput = Table(
        ("child", "expected"), // Headers

        ("'And it''s raining'", TSqlLexer.STRING),
        ("""'Tab\oir'""", TSqlLexer.STRING),
        ("""'Tab\'oir'""", TSqlLexer.STRING),
        ("'hello'", TSqlLexer.STRING),
        (""""quoted""id"""", TSqlLexer.DOUBLE_QUOTE_ID),
        ("\"quote\"\"andunquote\"\"\"", TSqlLexer.DOUBLE_QUOTE_ID))

      forAll(testInput) { (input: String, expected: Int) =>
        val inputString = CharStreams.fromString(input)

        lexer.setInputStream(inputString)
        val tok: Token = lexer.nextToken()
        tok.getType shouldBe expected
        tok.getText shouldBe input
      }
    }

  }

}
