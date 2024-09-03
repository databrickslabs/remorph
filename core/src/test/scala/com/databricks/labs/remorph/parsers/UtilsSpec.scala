package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.tsql.{TSqlLexer, TSqlParser}
import com.databricks.labs.remorph.utils.ParsingUtils
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.scalatest.wordspec.AnyWordSpec

class UtilsSpec extends AnyWordSpec {

  "Utils" should {
    "correctly collect text" in {
      val stream = CharStreams.fromString("SELECT * FROM table")
      val lexer = new TSqlLexer(stream)
      val parser = new TSqlParser(new CommonTokenStream(lexer))
      val result = parser.tSqlFile()
      val text = ParsingUtils.getTextFromParserRuleContext(result)
      assert(text == "SELECT * FROM table")
    }
  }
}
