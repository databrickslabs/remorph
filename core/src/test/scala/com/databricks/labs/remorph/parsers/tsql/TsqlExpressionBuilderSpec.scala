package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TsqlExpressionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

  private def example(query: String, expectedAst: TreeNode): Assertion =
    example(query, _.tsql_file(), expectedAst)

  "tsql expression builder" should {
    "translate a SELECT query with unary expressions" in {
      example(
        query = "SELECT -a FROM foo",
        expectedAst = Project(NamedTable("foo", Map.empty, is_streaming = false), Seq(Minus(Column("a")))))
      example(
        query = "SELECT +a FROM foo",
        expectedAst = Project(NamedTable("foo", Map.empty, is_streaming = false), Seq(Column("a"))))
      example(
        query = "SELECT ~a FROM foo",
        expectedAst = Project(NamedTable("foo", Map.empty, is_streaming = false), Seq(Not(Column("a")))))
    }
  }
}
