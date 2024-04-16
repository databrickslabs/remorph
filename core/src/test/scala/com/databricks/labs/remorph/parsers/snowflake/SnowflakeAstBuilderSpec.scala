package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeAstBuilderSpec extends AnyWordSpec with Matchers {

  private def parseString(input: String): SnowflakeParser.Snowflake_fileContext = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val tree = parser.snowflake_file()
    // uncomment the following line if you need a peek in the Snowflake AST
    // println(tree.toStringTree(parser))
    tree
  }

  private def example(query: String, expectedAst: TreeNode): Assertion = {
    val sfTree = parseString(query)

    val result = new SnowflakeAstBuilder().visit(sfTree)

    result shouldBe expectedAst
  }

  "SnowflakeVisitor" should {
    "translate a simple SELECT query" in {
      example(
        query = "SELECT a FROM b",
        expectedAst = Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Column("a"))))
    }

    "translate a simple SELECT query with an aliased column" in {

      example(
        query = "SELECT a AS aa FROM b",
        expectedAst =
          Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Alias(Column("a"), Seq("aa"), None))))
    }

    "translate a simple SELECT query involving multiple columns" in {

      example(
        query = "SELECT a, b, c FROM table_x",
        expectedAst =
          Project(NamedTable("table_x", Map.empty, is_streaming = false), Seq(Column("a"), Column("b"), Column("c"))))
    }

    "translate a SELECT query involving multiple columns and aliases" in {

      example(
        query = "SELECT a, b AS bb, c FROM table_x",
        expectedAst = Project(
          NamedTable("table_x", Map.empty, is_streaming = false),
          Seq(Column("a"), Alias(Column("b"), Seq("bb"), None), Column("c"))))
    }

    val simpleJoinAst =
      Join(
        NamedTable("table_x", Map.empty, is_streaming = false),
        NamedTable("table_y", Map.empty, is_streaming = false),
        join_condition = None,
        InnerJoin,
        using_columns = Seq(),
        JoinDataType(is_left_struct = false, is_right_struct = false))

    "translate a query with a JOIN" in {
      example(query = "SELECT a FROM table_x JOIN table_y", expectedAst = Project(simpleJoinAst, Seq(Column("a"))))
    }

    // TODO: fix the grammar (LEFT gets parsed as an alias rather than a join_type)
    "translate a query with a LEFT JOIN" ignore {
      example(
        query = "SELECT a FROM table_x LEFT JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = LeftOuterJoin), Seq(Column("a"))))
    }

    "translate a query with a LEFT OUTER JOIN" in {
      example(
        query = "SELECT a FROM table_x LEFT OUTER JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = LeftOuterJoin), Seq(Column("a"))))
    }

    // TODO: fix the grammar (RIGHT gets parsed as an alias rather than a join_type)
    "translate a query with a RIGHT JOIN" ignore {
      example(
        query = "SELECT a FROM table_x RIGHT JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = RightOuterJoin), Seq(Column("a"))))
    }

    "translate a query with a RIGHT OUTER JOIN" in {
      example(
        query = "SELECT a FROM table_x RIGHT OUTER JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = RightOuterJoin), Seq(Column("a"))))
    }

    "translate a query with a FULL JOIN" in {
      example(
        query = "SELECT a FROM table_x FULL JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = FullOuterJoin), Seq(Column("a"))))
    }

    "translate a query with a simple WHERE clause" in {
      val expectedOperatorTranslations = List(
        "=" -> Equals(Column("a"), Column("b")),
        "!=" -> NotEquals(Column("a"), Column("b")),
        "<>" -> NotEquals(Column("a"), Column("b")),
        ">" -> GreaterThan(Column("a"), Column("b")),
        "<" -> LesserThan(Column("a"), Column("b")),
        ">=" -> GreaterThanOrEqual(Column("a"), Column("b")),
        "<=" -> LesserThanOrEqual(Column("a"), Column("b")))

      expectedOperatorTranslations.foreach { case (op, expectedPredicate) =>
        example(
          query = s"SELECT a, b FROM c WHERE a $op b",
          expectedAst = Project(
            Filter(NamedTable("c", Map.empty, is_streaming = false), expectedPredicate),
            Seq(Column("a"), Column("b"))))
      }
    }

    "translate a query with a WHERE clause involving composite predicates" in {
      example(
        query = "SELECT a, b FROM c WHERE a = b AND b = a",
        expectedAst = Project(
          Filter(
            NamedTable("c", Map.empty, is_streaming = false),
            And(Equals(Column("a"), Column("b")), Equals(Column("b"), Column("a")))),
          Seq(Column("a"), Column("b"))))

      example(
        query = "SELECT a, b FROM c WHERE a = b OR b = a",
        expectedAst = Project(
          Filter(
            NamedTable("c", Map.empty, is_streaming = false),
            Or(Equals(Column("a"), Column("b")), Equals(Column("b"), Column("a")))),
          Seq(Column("a"), Column("b"))))

      example(
        query = "SELECT a, b FROM c WHERE NOT a = b",
        expectedAst = Project(
          Filter(NamedTable("c", Map.empty, is_streaming = false), Not(Equals(Column("a"), Column("b")))),
          Seq(Column("a"), Column("b"))))
    }

    "translate a query with a GROUP BY clause" in {
      example(
        query = "SELECT a, COUNT(b) FROM c GROUP BY a",
        expectedAst = Project(
          Aggregate(
            input = NamedTable("c", Map.empty, is_streaming = false),
            group_type = GroupBy,
            grouping_expressions = Seq(Column("a")),
            pivot = None),
          Seq(Column("a"), Count(Column("b")))))
    }

    "translate a query with a GROUP BY and ORDER BY clauses" in {
      example(
        query = "SELECT a, COUNT(b) FROM c GROUP BY a ORDER BY a",
        expectedAst = Project(
          Sort(
            Aggregate(
              input = NamedTable("c", Map.empty, is_streaming = false),
              group_type = GroupBy,
              grouping_expressions = Seq(Column("a")),
              pivot = None),
            Seq(SortOrder(Column("a"), AscendingSortDirection, SortNullsLast)),
            is_global = false),
          Seq(Column("a"), Count(Column("b")))))
    }

    "translate a query with ORDER BY" in {
      example(
        query = "SELECT a FROM b ORDER BY a",
        expectedAst = Project(
          Sort(
            input = NamedTable("b", Map.empty, is_streaming = false),
            order = Seq(SortOrder(Column("a"), AscendingSortDirection, SortNullsLast)),
            is_global = false),
          Seq(Column("a"))))

      example(
        query = "SELECT a FROM b ORDER BY a DESC",
        expectedAst = Project(
          Sort(
            input = NamedTable("b", Map.empty, is_streaming = false),
            order = Seq(SortOrder(Column("a"), DescendingSortDirection, SortNullsLast)),
            is_global = false),
          Seq(Column("a"))))

      example(
        query = "SELECT a FROM b ORDER BY a NULLS FIRST",
        expectedAst = Project(
          Sort(
            input = NamedTable("b", Map.empty, is_streaming = false),
            order = Seq(SortOrder(Column("a"), AscendingSortDirection, SortNullsFirst)),
            is_global = false),
          Seq(Column("a"))))

      example(
        query = "SELECT a FROM b ORDER BY a DESC NULLS FIRST",
        expectedAst = Project(
          Sort(
            input = NamedTable("b", Map.empty, is_streaming = false),
            order = Seq(SortOrder(Column("a"), DescendingSortDirection, SortNullsFirst)),
            is_global = false),
          Seq(Column("a"))))
    }

    "translate queries with LIMIT and OFFSET" in {
      example(
        query = "SELECT a FROM b LIMIT 5",
        expectedAst = Project(Limit(NamedTable("b", Map.empty, is_streaming = false), 5), Seq(Column("a"))))
      example(
        query = "SELECT a FROM b LIMIT 5 OFFSET 10",
        expectedAst = Project(Offset(Limit(NamedTable("b", Map.empty, is_streaming = false), 5), 10), Seq(Column("a"))))
    }
  }
}
