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

    "translate a query with a JOIN" in {
      val joinCondition = And(Equals(Column("A"), Column("A")), Equals(Column("B"), Column("B")))

      val joinAst = Join(
        NamedTable("DBO.TABLE_X", Map(), false),
        NamedTable("DBO.TABLE_Y", Map(), false),
        Some(joinCondition),
        InnerJoin,
        Seq(),
        JoinDataType(false, false))

      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A AND T1.B = T2.B",
        expectedAst = Project(joinAst, Seq(Column("A"), Column("B"))))
    }

    "translate a query with Multiple JOIN AND Condition" in {
      val joinConditionX = Equals(Column("A"), Column("A"))
      val joinConditionZ = And(Equals(Column("A"), Column("A")), Equals(Column("B"), Column("B")))

      val joinFirstAst = Join(
        NamedTable("DBO.TABLE_X", Map(), false),
        NamedTable("DBO.TABLE_Y", Map(), false),
        Some(joinConditionX),
        InnerJoin,
        Seq(),
        JoinDataType(false, false))

      val joinMainAst = Join(
        joinFirstAst,
        NamedTable("DBO.TABLE_Z", Map(), false),
        Some(joinConditionZ),
        LeftOuterJoin,
        Seq(),
        JoinDataType(false, false))

      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A " +
          "LEFT JOIN DBO.TABLE_Z AS T3 ON T1.A = T3.A AND T1.B = T3.B",
        expectedAst = Project(joinMainAst, Seq(Column("A"), Column("B"))))
    }

    "translate a query with Multiple JOIN OR Condition" in {
      val joinConditionX = Equals(Column("A"), Column("A"))
      val joinConditionZ = Or(Equals(Column("A"), Column("A")), Equals(Column("B"), Column("B")))

      val joinFirstAst = Join(
        NamedTable("DBO.TABLE_X", Map(), false),
        NamedTable("DBO.TABLE_Y", Map(), false),
        Some(joinConditionX),
        InnerJoin,
        Seq(),
        JoinDataType(false, false))

      val joinMainAst = Join(
        joinFirstAst,
        NamedTable("DBO.TABLE_Z", Map(), false),
        Some(joinConditionZ),
        LeftOuterJoin,
        Seq(),
        JoinDataType(false, false))

      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A " +
          "LEFT JOIN DBO.TABLE_Z AS T3 ON T1.A = T3.A OR T1.B = T3.B",
        expectedAst = Project(joinMainAst, Seq(Column("A"), Column("B"))))

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
