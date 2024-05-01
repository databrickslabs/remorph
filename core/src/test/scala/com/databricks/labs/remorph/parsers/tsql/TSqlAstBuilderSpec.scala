package com.databricks.labs.remorph.parsers.tsql

import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import com.databricks.labs.remorph.parsers.intermediate._

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
      "translate constants in selects with no table" in {
        example(
          query = "SELECT 42, 6.4, 0x5A, 2.7E9, $40",
          expectedAst = Project(
            NoTable(),
            Seq(
              Literal(integer = Some(42)),
              Literal(float = Some(6.4f)),
              Literal(string = Some("0x5A")),
              Literal(double = Some(2.7e9)),
              UnresolvedExpression("$40"))))
      }
    }
  }
  "translate SELECT queries with binary expressions" in {
    example(
      query = "SELECT a + b FROM dbo.table_x",
      expectedAst =
        Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Add(Column("a"), Column("b")))))

    example(
      query = "SELECT a - b FROM dbo.table_x",
      expectedAst =
        Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Subtract(Column("a"), Column("b")))))

    example(
      query = "SELECT a * b FROM dbo.table_x",
      expectedAst =
        Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Multiply(Column("a"), Column("b")))))

    example(
      query = "SELECT a / b FROM dbo.table_x",
      expectedAst =
        Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Divide(Column("a"), Column("b")))))

    example(
      query = "SELECT a || b FROM dbo.table_x",
      expectedAst =
        Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Concat(Column("a"), Column("b")))))

  }
}
