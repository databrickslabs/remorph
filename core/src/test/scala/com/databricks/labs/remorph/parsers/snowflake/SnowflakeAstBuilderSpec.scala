package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeAstBuilderSpec extends AnyWordSpec with ParserTestCommon with Matchers {

  override def astBuilder: SnowflakeParserBaseVisitor[_] = new SnowflakeAstBuilder
  private def example(query: String, expectedAst: TreeNode): Assertion =
    example(query, _.snowflake_file(), expectedAst)

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

    "translate a query with GROUP BY HAVING clause" in {
      example(
        query = "SELECT a, COUNT(b) FROM c GROUP BY a HAVING COUNT(b) > 1",
        expectedAst = Project(
          Filter(
            Aggregate(
              input = NamedTable("c", Map.empty, is_streaming = false),
              group_type = GroupBy,
              grouping_expressions = Seq(Column("a")),
              pivot = None),
            GreaterThan(Count(Column("b")), Literal(integer = Some(1)))),
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
    "translate a query with PIVOT" in {
      example(
        query = "SELECT a FROM b PIVOT (SUM(a) FOR c IN ('foo', 'bar'))",
        expectedAst = Project(
          Aggregate(
            input = NamedTable("b", Map.empty, is_streaming = false),
            group_type = Pivot,
            grouping_expressions = Seq(Sum(Column("a"))),
            pivot = Some(Pivot(Column("c"), Seq(Literal(string = Some("foo")), Literal(string = Some("bar")))))),
          Seq(Column("a"))))
    }

    "translate a query with UNPIVOT" in {
      example(
        query = "SELECT a FROM b UNPIVOT (c FOR d IN (e, f))",
        expectedAst = Project(
          Unpivot(
            input = NamedTable("b", Map.empty, is_streaming = false),
            ids = Seq(Column("e"), Column("f")),
            values = None,
            variable_column_name = "c",
            value_column_name = "d"),
          Seq(Column("a"))))
    }

    "translate queries with WITH clauses" in {
      example(
        query = "WITH a (b, c, d) AS (SELECT x, y, z FROM e) SELECT b, c, d FROM a",
        expectedAst = WithCTE(
          Seq(
            CTEDefinition(
              tableName = "a",
              columns = Seq(Column("b"), Column("c"), Column("d")),
              cte = Project(namedTable("e"), Seq(Column("x"), Column("y"), Column("z"))))),
          Project(namedTable("a"), Seq(Column("b"), Column("c"), Column("d")))))

      example(
        query =
          "WITH a (b, c, d) AS (SELECT x, y, z FROM e), aa (bb, cc) AS (SELECT xx, yy FROM f) SELECT b, c, d FROM a",
        expectedAst = WithCTE(
          Seq(
            CTEDefinition(
              tableName = "a",
              columns = Seq(Column("b"), Column("c"), Column("d")),
              cte = Project(namedTable("e"), Seq(Column("x"), Column("y"), Column("z")))),
            CTEDefinition(
              tableName = "aa",
              columns = Seq(Column("bb"), Column("cc")),
              cte = Project(namedTable("f"), Seq(Column("xx"), Column("yy"))))),
          Project(namedTable("a"), Seq(Column("b"), Column("c"), Column("d")))))
    }

    "translate a query with WHERE, GROUP BY, HAVING, QUALIFY" in {
      example(
        query = """SELECT c2, SUM(c3) OVER (PARTITION BY c2) as r
                  |  FROM t1
                  |  WHERE c3 < 4
                  |  GROUP BY c2, c3
                  |  HAVING AVG(c1) >= 5
                  |  QUALIFY MIN(r) > 6""".stripMargin,
        expectedAst = Project(
          Filter(
            Filter(
              Aggregate(
                input = Filter(namedTable("t1"), LesserThan(Column("c3"), Literal(integer = Some(4)))),
                group_type = GroupBy,
                grouping_expressions = Seq(Column("c2"), Column("c3")),
                pivot = None),
              GreaterThanOrEqual(Avg(Column("c1")), Literal(integer = Some(5)))),
            GreaterThan(Min(Column("r")), Literal(integer = Some(6)))),
          Seq(
            Column("c2"),
            Alias(Window(Sum(Column("c3")), Seq(Column("c2")), Seq(), DummyWindowFrame), Seq("r"), None))))
    }

    "translate a query with set operators" in {
      example(
        "SELECT a FROM t1 UNION SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(Column("a"))),
          Project(namedTable("t2"), Seq(Column("b"))),
          UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      example(
        "SELECT a FROM t1 UNION ALL SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(Column("a"))),
          Project(namedTable("t2"), Seq(Column("b"))),
          UnionSetOp,
          is_all = true,
          by_name = false,
          allow_missing_columns = false))
      example(
        "SELECT a FROM t1 MINUS SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(Column("a"))),
          Project(namedTable("t2"), Seq(Column("b"))),
          ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      example(
        "SELECT a FROM t1 EXCEPT SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(Column("a"))),
          Project(namedTable("t2"), Seq(Column("b"))),
          ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))

      example(
        "SELECT a FROM t1 INTERSECT SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(Column("a"))),
          Project(namedTable("t2"), Seq(Column("b"))),
          IntersectSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))

      example(
        "SELECT a FROM t1 INTERSECT SELECT b FROM t2 MINUS SELECT c FROM t3 UNION SELECT d FROM t4",
        SetOperation(
          SetOperation(
            SetOperation(
              Project(namedTable("t1"), Seq(Column("a"))),
              Project(namedTable("t2"), Seq(Column("b"))),
              IntersectSetOp,
              is_all = false,
              by_name = false,
              allow_missing_columns = false),
            Project(namedTable("t3"), Seq(Column("c"))),
            ExceptSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          Project(namedTable("t4"), Seq(Column("d"))),
          UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
    }
  }
}
