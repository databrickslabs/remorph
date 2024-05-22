package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlAstBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

  private def example(query: String, expectedAst: TreeNode): Assertion =
    example(query, _.tSqlFile(), expectedAst)

  "tsql visitor" should {

    "accept empty input" in {
      example(query = "", expectedAst = Batch(Seq.empty))
    }

    "translate a simple SELECT query" in {
      example(
        query = "SELECT a FROM dbo.table_x",
        expectedAst = Batch(Seq(Project(NamedTable("dbo.table_x", Map.empty, is_streaming = false), Seq(Column("a"))))))
    }

    "translate column aliases" in {
      example(
        query = "SELECT a AS b, J = BigCol FROM dbo.table_x",
        expectedAst = Batch(
          Seq(
            Project(
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              Seq(Alias(Column("a"), Seq("b"), None), Alias(Column("BigCol"), Seq("J"), None))))))
    }

    "accept constants in selects" in {
      example(
        query = "SELECT 42, 6.4, 0x5A, 2.7E9, 4.24523534425245E10, $40",
        expectedAst = Batch(
          Seq(Project(
            NoTable(),
            Seq(
              Literal(integer = Some(42)),
              Literal(float = Some(6.4f)),
              Literal(string = Some("0x5A")),
              Literal(long = Some(2700000000L)),
              Literal(double = Some(4.24523534425245e10)),
              Money(Literal(string = Some("$40"))))))))
    }

    "translate collation specifiers" in {
      example(
        query = "SELECT a COLLATE Latin1_General_BIN FROM dbo.table_x",
        expectedAst = Batch(
          Seq(
            Project(
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              Seq(Collate(Column("a"), "Latin1_General_BIN"))))))
    }

    "translate table source items with aliases" in {
      example(
        query = "SELECT a FROM dbo.table_x AS t",
        expectedAst = Batch(
          Seq(Project(TableAlias(NamedTable("dbo.table_x", Map.empty, is_streaming = false), "t"), Seq(Column("a"))))))
    }

    "infer a cross join" in {
      example(
        query = "SELECT a, b, c FROM dbo.table_x, dbo.table_y",
        expectedAst = Batch(
          Seq(Project(
            Join(
              NamedTable("dbo.table_x", Map.empty, is_streaming = false),
              NamedTable("dbo.table_y", Map.empty, is_streaming = false),
              None,
              CrossJoin,
              Seq.empty,
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            Seq(Column("a"), Column("b"), Column("c"))))))
    }
    "translate a query with a JOIN" in {
      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A AND T1.B = T2.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
              Some(And(Equals(Column("T1.A"), Column("T2.A")), Equals(Column("T1.B"), Column("T2.B")))),
              InnerJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"), Column("T2.B"))))))
    }
    "translate a query with Multiple JOIN AND Condition" in {
      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A " +
          "LEFT JOIN DBO.TABLE_Z AS T3 ON T1.A = T3.A AND T1.B = T3.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              Join(
                TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
                TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
                Some(Equals(Column("T1.A"), Column("T2.A"))),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(NamedTable("DBO.TABLE_Z", Map(), is_streaming = false), "T3"),
              Some(And(Equals(Column("T1.A"), Column("T3.A")), Equals(Column("T1.B"), Column("T3.B")))),
              LeftOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"), Column("T2.B"))))))
    }
    "translate a query with Multiple JOIN OR Conditions" in {
      example(
        query = "SELECT T1.A, T2.B FROM DBO.TABLE_X AS T1 INNER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A " +
          "LEFT JOIN DBO.TABLE_Z AS T3 ON T1.A = T3.A OR T1.B = T3.B",
        expectedAst = Batch(
          Seq(Project(
            Join(
              Join(
                TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
                TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
                Some(Equals(Column("T1.A"), Column("T2.A"))),
                InnerJoin,
                List(),
                JoinDataType(is_left_struct = false, is_right_struct = false)),
              TableAlias(NamedTable("DBO.TABLE_Z", Map(), is_streaming = false), "T3"),
              Some(Or(Equals(Column("T1.A"), Column("T3.A")), Equals(Column("T1.B"), Column("T3.B")))),
              LeftOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"), Column("T2.B"))))))
    }
    "translate a query with a RIGHT OUTER JOIN" in {
      example(
        query = "SELECT T1.A FROM DBO.TABLE_X AS T1 RIGHT OUTER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
              Some(Equals(Column("T1.A"), Column("T2.A"))),
              RightOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"))))))
    }
    "translate a query with a FULL OUTER JOIN" in {
      example(
        query = "SELECT T1.A FROM DBO.TABLE_X AS T1 FULL OUTER JOIN DBO.TABLE_Y AS T2 ON T1.A = T2.A",
        expectedAst = Batch(
          Seq(Project(
            Join(
              TableAlias(NamedTable("DBO.TABLE_X", Map(), is_streaming = false), "T1"),
              TableAlias(NamedTable("DBO.TABLE_Y", Map(), is_streaming = false), "T2"),
              Some(Equals(Column("T1.A"), Column("T2.A"))),
              FullOuterJoin,
              List(),
              JoinDataType(is_left_struct = false, is_right_struct = false)),
            List(Column("T1.A"))))))
    }
  }
}
