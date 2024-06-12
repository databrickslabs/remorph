package com.databricks.labs.remorph.parsers.tsql

import org.antlr.v4.runtime.{CharStreams, Token}
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.wordspec.AnyWordSpec

class TSqlLexerSpec extends AnyWordSpec with Matchers with TableDrivenPropertyChecks {

  private val lexer = new TSqlLexer(null)

  "TSqlLexer" should {
    "parse string literals" in {

      val testInput = Table(
        ("input", "expected"), // Headers
        (""""quoted""id""", TSqlLexer.DOUBLE_QUOTE_ID),
        (" \"quote\"\"andunquote\"\"\"", TSqlLexer.DOUBLE_QUOTE_ID),
        ("\"quote\"\"andunquote\"\"\"", TSqlLexer.DOUBLE_QUOTE_ID),
        ("'hello'", TSqlLexer.STRING))

      forAll(testInput) { (input: String, expected: Int) =>
        val inputString = CharStreams.fromString(input)

        lexer.setInputStream(inputString)
        val tok: Token = lexer.nextToken()
        tok.getType should be(expected)
      }
    }

  }

}
