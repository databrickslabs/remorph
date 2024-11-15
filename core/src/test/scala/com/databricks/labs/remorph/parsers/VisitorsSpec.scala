package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.intermediate.{TreeNode, WithKnownLocationRange}
import com.databricks.labs.remorph.parsers.tsql.{TSqlLexer, TSqlParser, TSqlParserBaseVisitor, TSqlVisitorCoordinator}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.scalatest.wordspec.AnyWordSpec

case class FakeNode(value: String) extends TreeNode[FakeNode] {
  override def children: Seq[FakeNode] = Seq.empty
}

class FakeVisitor(override val vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[WithKnownLocationRange[FakeNode]]
    with ParserCommon[FakeNode] {
  override protected def unresolved(ruleText: String, message: String): FakeNode = FakeNode(ruleText)
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
