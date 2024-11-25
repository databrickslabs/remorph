package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.tsql.{TSqlLexer, TSqlParser, TSqlParserBaseVisitor, TSqlVisitorCoordinator}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.scalatest.wordspec.AnyWordSpec

class FakeVisitor(override val vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[String]
    with ParserCommon[String] {
  override protected def unresolved(ruleText: String, message: String): String = ruleText
}

class VistorsSpec extends AnyWordSpec {

  "Visitors" should {
    "correctly collect text from contexts" in {
      val stream = CharStreams.fromString("SELECT * FROM table;")
      val result = new TSqlParser(new CommonTokenStream(new TSqlLexer(stream))).tSqlFile()
      val text = new FakeVisitor(null).contextText(result)
      assert(text == "SELECT * FROM table;")
    }
  }
}
