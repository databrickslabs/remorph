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

    example(query = "SELECT a % b", expectedAst = Project(NoTable(), Seq(Mod(Column("a"), Column("b")))))

    example(query = "SELECT a & b", expectedAst = Project(NoTable(), Seq(BitwiseAnd(Column("a"), Column("b")))))

    example(query = "SELECT a | b", expectedAst = Project(NoTable(), Seq(BitwiseOr(Column("a"), Column("b")))))

    example(query = "SELECT a ^ b", expectedAst = Project(NoTable(), Seq(BitwiseXor(Column("a"), Column("b")))))
  }
  "translate queries with complex expressions, including parens" in {
    example(
      query = "SELECT a + b * 2",
      expectedAst = Project(NoTable(), Seq(Add(Column("a"), Multiply(Column("b"), Literal(integer = Some(2)))))))

    example(
      query = "SELECT (a + b) * 2",
      expectedAst = Project(NoTable(), Seq(Multiply(Add(Column("a"), Column("b")), Literal(integer = Some(2))))))

    example(
      query = "SELECT a & b | c",
      expectedAst = Project(NoTable(), Seq(BitwiseOr(BitwiseAnd(Column("a"), Column("b")), Column("c")))))

    example(
      query = "SELECT (a & b) | c",
      expectedAst = Project(NoTable(), Seq(BitwiseOr(BitwiseAnd(Column("a"), Column("b")), Column("c")))))

    example(
      query = "SELECT a % 3 + b * 2 - c / 5",
      expectedAst = Project(
        NoTable(),
        Seq(
          Subtract(
            Add(Mod(Column("a"), Literal(integer = Some(3))), Multiply(Column("b"), Literal(integer = Some(2)))),
            Divide(Column("c"), Literal(integer = Some(5)))))))

    example(
      query = "SELECT (a % 3 + b) * 2 - c / 5",
      expectedAst = Project(
        NoTable(),
        Seq(
          Subtract(
            Multiply(Add(Mod(Column("a"), Literal(integer = Some(3))), Column("b")), Literal(integer = Some(2))),
            Divide(Column("c"), Literal(integer = Some(5)))))))
    example(query = "SELECT a || b", expectedAst = Project(NoTable(), Seq(Concat(Column("a"), Column("b")))))

    example(
      query = "SELECT a || b || c",
      expectedAst = Project(NoTable(), Seq(Concat(Concat(Column("a"), Column("b")), Column("c")))))
  }
}
