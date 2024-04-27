package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlAstBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

  private def example(query: String, expectedAst: TreeNode): Assertion =
    example(query, _.tsql_file(), expectedAst)

  "tsql visitor" should {
    "translate a simple SELECT query" in {
      example(
        query = "SELECT a FROM dbo.table_x",
        expectedAst = Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Column("a"))))
    }
    "tsql visitor" should {
      "accept constants in selects" in {
        example(
          query = "SELECT 42, 6.4, 0x5A, 2.7E9, $40 FROM dbo.table_x",
          expectedAst = Project(
            NamedTable("dbo.table_x", Map.empty, is_streaming = false),
            Seq(
              Literal(integer = Some(42)),
              Literal(float = Some(6.4f)),
              Literal(string = Some("0x5A")),
              Literal(double = Some(2.7e9)),
              UnresolvedExpression("$40"))))
      }
    }
  }
}
