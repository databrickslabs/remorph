package com.databricks.labs.remorph.parsers.snowflake

import org.antlr.v4.runtime.{CharStreams, Token}
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.wordspec.AnyWordSpec

class SnowLexerSpec extends AnyWordSpec with Matchers with TableDrivenPropertyChecks {

  private val lexer = new SnowflakeLexer(null)

  private def fillTokens(input: String): List[Token] = {
    val inputString = CharStreams.fromString(input)
    lexer.setInputStream(inputString)
    Iterator.continually(lexer.nextToken()).takeWhile(_.getType != Token.EOF).toList
  }

  private def dumpTokens(tokens: List[Token]): Unit = {
    tokens.foreach { t =>
      // scalastyle:off println
      val name = lexer.getVocabulary.getDisplayName(t.getType).padTo(32, ' ')
      println(s"${name}(${t.getType}) -->${t.getText}<--")
      // scalastyle:on println
    }
  }

  // TODO: Expand this test to cover all token types, and maybe all tokens
  "Snowflake Lexer" should {
    "scan string literals and ids" in {

      val testInput = Table(
        ("child", "expected"), // Headers

        (""""quoted""id"""", SnowflakeLexer.DOUBLE_QUOTE_ID),
        ("\"quote\"\"andunquote\"\"\"", SnowflakeLexer.DOUBLE_QUOTE_ID),
        ("identifier_1", SnowflakeLexer.ID),
        ("SELECT", SnowflakeLexer.SELECT),
        ("FROM", SnowflakeLexer.FROM),
        ("WHERE", SnowflakeLexer.WHERE),
        ("GROUP", SnowflakeLexer.GROUP),
        ("BY", SnowflakeLexer.BY),
        ("HAVING", SnowflakeLexer.HAVING),
        ("ORDER", SnowflakeLexer.ORDER),
        ("LIMIT", SnowflakeLexer.LIMIT),
        ("UNION", SnowflakeLexer.UNION),
        ("ALL", SnowflakeLexer.ALL),
        ("INTERSECT", SnowflakeLexer.INTERSECT),
        ("INSERT", SnowflakeLexer.INSERT),
        ("EXCEPT", SnowflakeLexer.EXCEPT),
        ("-", SnowflakeLexer.MINUS),
        ("+", SnowflakeLexer.PLUS),
        ("42", SnowflakeLexer.INT),
        ("42.42", SnowflakeLexer.FLOAT),
        ("42E4", SnowflakeLexer.REAL),
        ("!=", SnowflakeLexer.NE),
        ("*", SnowflakeLexer.STAR),
        ("/", SnowflakeLexer.DIVIDE),
        ("!ABORT", SnowflakeLexer.SQLCOMMAND),
        ("$parameter", SnowflakeLexer.LOCAL_ID),
        ("$ids", SnowflakeLexer.LOCAL_ID),
        ("=", SnowflakeLexer.EQ),
        ("!=", SnowflakeLexer.NE),
        (">", SnowflakeLexer.GT),
        ("<", SnowflakeLexer.LT),
        (">=", SnowflakeLexer.GE),
        ("<=", SnowflakeLexer.LE),
        ("(", SnowflakeLexer.LPAREN),
        (")", SnowflakeLexer.RPAREN),
        (",", SnowflakeLexer.COMMA),
        (";", SnowflakeLexer.SEMI),
        ("[", SnowflakeLexer.LSB),
        ("]", SnowflakeLexer.RSB),
        (":", SnowflakeLexer.COLON),
        ("::", SnowflakeLexer.COLON_COLON))

      forAll(testInput) { (input: String, expectedType: Int) =>
        val inputString = CharStreams.fromString(input)

        lexer.setInputStream(inputString)
        val tok: Token = lexer.nextToken()
        tok.getType shouldBe expectedType
        tok.getText shouldBe input
      }
    }

    "scan string literals with escaped solidus" in {
      val tok = fillTokens("""'\\'""")
      dumpTokens(tok)
      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_ESCAPE
      tok(1).getText shouldBe """\\"""

      tok(2).getType shouldBe SnowflakeLexer.STRING_END
      tok(2).getText shouldBe "'"

    }

    "scan string literals with double single quotes" in {
      val tok = fillTokens("'And it''s raining'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(1).getText shouldBe "And it"

      tok(2).getType shouldBe SnowflakeLexer.STRING_SQUOTE
      tok(2).getText shouldBe "''"

      tok(3).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(3).getText shouldBe "s raining"

      tok(4).getType shouldBe SnowflakeLexer.STRING_END
      tok(4).getText shouldBe "'"
    }

    "scan string literals with an escaped character" in {
      val tok = fillTokens("""'Tab\oir'""")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(1).getText shouldBe "Tab"

      tok(2).getType shouldBe SnowflakeLexer.STRING_ESCAPE
      tok(2).getText shouldBe "\\o"

      tok(3).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(3).getText shouldBe "ir"

      tok(4).getType shouldBe SnowflakeLexer.STRING_END
      tok(4).getText shouldBe "'"
    }

    "scan string literals with an escaped single quote" in {
      val tok = fillTokens("""'Tab\'oir'""")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(1).getText shouldBe "Tab"

      tok(2).getType shouldBe SnowflakeLexer.STRING_ESCAPE
      tok(2).getText shouldBe "\\'"

      tok(3).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(3).getText shouldBe "oir"

      tok(4).getType shouldBe SnowflakeLexer.STRING_END
      tok(4).getText shouldBe "'"
    }

    "scan string literals with an embedded Unicode escape" in {
      val tok = fillTokens("'Tab\\" + "uAcDcbaT'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(1).getText shouldBe "Tab"

      tok(2).getType shouldBe SnowflakeLexer.STRING_UNICODE
      tok(2).getText shouldBe "\\uAcDc"

      tok(3).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(3).getText shouldBe "baT"

      tok(4).getType shouldBe SnowflakeLexer.STRING_END
      tok(4).getText shouldBe "'"
    }

    "scan simple &variables" in {
      val tok = fillTokens("&leeds")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.AMP
      tok.head.getText shouldBe "&"

      tok(1).getType shouldBe SnowflakeLexer.ID
      tok(1).getText shouldBe "leeds"
    }

    "scan simple consecutive &variables" in {
      val tok = fillTokens("&leeds&manchester")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.AMP
      tok.head.getText shouldBe "&"

      tok(1).getType shouldBe SnowflakeLexer.ID
      tok(1).getText shouldBe "leeds"

      tok(2).getType shouldBe SnowflakeLexer.AMP
      tok(2).getText shouldBe "&"

      tok(3).getType shouldBe SnowflakeLexer.ID
      tok(3).getText shouldBe "manchester"
    }

    "scan simple &variables within composite variables" in {
      lexer.setInputStream(CharStreams.fromString("&leeds.&manchester"))
      val tok = fillTokens("&leeds.&manchester")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.AMP
      tok.head.getText shouldBe "&"

      tok(1).getType shouldBe SnowflakeLexer.ID
      tok(1).getText shouldBe "leeds"

      tok(2).getType shouldBe SnowflakeLexer.DOT
      tok(2).getText shouldBe "."

      tok(3).getType shouldBe SnowflakeLexer.AMP
      tok(3).getText shouldBe "&"

      tok(4).getType shouldBe SnowflakeLexer.ID
      tok(4).getText shouldBe "manchester"
    }

    "scan && in a string" in {
      val tok = fillTokens("'&&notAVar'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_AMPAMP
      tok(1).getText shouldBe "&&"

      tok(2).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(2).getText shouldBe "notAVar"

      tok(3).getType shouldBe SnowflakeLexer.STRING_END
      tok(3).getText shouldBe "'"
    }

    "scan && in a string with {}" in {
      val tok = fillTokens("'&&{notAVar}'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_AMPAMP
      tok(1).getText shouldBe "&&"

      tok(2).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(2).getText shouldBe "{notAVar}"

      tok(3).getType shouldBe SnowflakeLexer.STRING_END
      tok(3).getText shouldBe "'"
    }
    "scan &variables in a string" in {
      val tok = fillTokens("'&leeds'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.VAR_SIMPLE
      tok(1).getText shouldBe "&leeds"

      tok(2).getType shouldBe SnowflakeLexer.STRING_END
      tok(2).getText shouldBe "'"
    }

    "scan consecutive &variables in a string" in {
      val tok = fillTokens("'&leeds&{united}'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.VAR_SIMPLE
      tok(1).getText shouldBe "&leeds"

      tok(2).getType shouldBe SnowflakeLexer.VAR_COMPLEX
      tok(2).getText shouldBe "&{united}"

      tok(3).getType shouldBe SnowflakeLexer.STRING_END
      tok(3).getText shouldBe "'"
    }

    "scan &variables separated by && in a string" in {
      val tok = fillTokens("'&leeds&&&united'")
      dumpTokens(tok)

      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.VAR_SIMPLE
      tok(1).getText shouldBe "&leeds"

      tok(2).getType shouldBe SnowflakeLexer.STRING_AMPAMP
      tok(2).getText shouldBe "&&"

      tok(3).getType shouldBe SnowflakeLexer.VAR_SIMPLE
      tok(3).getText shouldBe "&united"

      tok(4).getType shouldBe SnowflakeLexer.STRING_END
      tok(4).getText shouldBe "'"
    }

    "scan a single ampersand in a string" in {
      val tok = fillTokens("'&'")
      dumpTokens(tok)
      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(1).getText shouldBe "&"

      tok(2).getType shouldBe SnowflakeLexer.STRING_END
      tok(2).getText shouldBe "'"

    }

    "scan a trailing ampersand in a string" in {
      val tok = fillTokens("'&score&'")
      dumpTokens(tok)
      tok.head.getType shouldBe SnowflakeLexer.STRING_START
      tok.head.getText shouldBe "'"

      tok(1).getType shouldBe SnowflakeLexer.VAR_SIMPLE
      tok(1).getText shouldBe "&score"

      tok(2).getType shouldBe SnowflakeLexer.STRING_CONTENT
      tok(2).getText shouldBe "&"

      tok(3).getType shouldBe SnowflakeLexer.STRING_END
      tok(3).getText shouldBe "'"
    }
  }
}
