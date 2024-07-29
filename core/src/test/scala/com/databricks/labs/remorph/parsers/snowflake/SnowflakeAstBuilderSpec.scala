package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeAstBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder = new SnowflakeAstBuilder

  private def singleQueryExample(query: String, expectedAst: LogicalPlan) =
    example(query, _.snowflakeFile(), Batch(Seq(expectedAst)))

  "SnowflakeAstBuilder" should {
    "translate a simple SELECT query" in {
      singleQueryExample(
        query = "SELECT a FROM TABLE",
        expectedAst = Project(NamedTable("TABLE", Map.empty, is_streaming = false), Seq(simplyNamedColumn("a"))))
    }

    "translate a simple SELECT query with an aliased column" in {

      singleQueryExample(
        query = "SELECT a AS aa FROM b",
        expectedAst = Project(
          NamedTable("b", Map.empty, is_streaming = false),
          Seq(Alias(simplyNamedColumn("a"), Seq(Id("aa")), None))))
    }

    "translate a simple SELECT query involving multiple columns" in {

      singleQueryExample(
        query = "SELECT a, b, c FROM table_x",
        expectedAst = Project(
          NamedTable("table_x", Map.empty, is_streaming = false),
          Seq(simplyNamedColumn("a"), simplyNamedColumn("b"), simplyNamedColumn("c"))))
    }

    "translate a SELECT query involving multiple columns and aliases" in {

      singleQueryExample(
        query = "SELECT a, b AS bb, c FROM table_x",
        expectedAst = Project(
          NamedTable("table_x", Map.empty, is_streaming = false),
          Seq(simplyNamedColumn("a"), Alias(simplyNamedColumn("b"), Seq(Id("bb")), None), simplyNamedColumn("c"))))
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
      singleQueryExample(
        query = "SELECT a FROM table_x JOIN table_y",
        expectedAst = Project(simpleJoinAst, Seq(simplyNamedColumn("a"))))
    }

    "translate a query with a LEFT JOIN" in {
      singleQueryExample(
        query = "SELECT a FROM table_x LEFT JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = LeftOuterJoin), Seq(simplyNamedColumn("a"))))
    }

    "translate a query with a LEFT OUTER JOIN" in {
      singleQueryExample(
        query = "SELECT a FROM table_x LEFT OUTER JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = LeftOuterJoin), Seq(simplyNamedColumn("a"))))
    }

    "translate a query with a RIGHT JOIN" in {
      singleQueryExample(
        query = "SELECT a FROM table_x RIGHT JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = RightOuterJoin), Seq(simplyNamedColumn("a"))))
    }

    "translate a query with a RIGHT OUTER JOIN" in {
      singleQueryExample(
        query = "SELECT a FROM table_x RIGHT OUTER JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = RightOuterJoin), Seq(simplyNamedColumn("a"))))
    }

    "translate a query with a FULL JOIN" in {
      singleQueryExample(
        query = "SELECT a FROM table_x FULL JOIN table_y",
        expectedAst = Project(simpleJoinAst.copy(join_type = FullOuterJoin), Seq(simplyNamedColumn("a"))))
    }

    "translate a query with a simple WHERE clause" in {
      val expectedOperatorTranslations = List(
        "=" -> Equals(Id("a"), Id("b")),
        "!=" -> NotEquals(Id("a"), Id("b")),
        "<>" -> NotEquals(Id("a"), Id("b")),
        ">" -> GreaterThan(Id("a"), Id("b")),
        "<" -> LessThan(Id("a"), Id("b")),
        ">=" -> GreaterThanOrEqual(Id("a"), Id("b")),
        "<=" -> LessThanOrEqual(Id("a"), Id("b")))

      expectedOperatorTranslations.foreach { case (op, expectedPredicate) =>
        singleQueryExample(
          query = s"SELECT a, b FROM c WHERE a $op b",
          expectedAst = Project(
            Filter(NamedTable("c", Map.empty, is_streaming = false), expectedPredicate),
            Seq(simplyNamedColumn("a"), simplyNamedColumn("b"))))
      }
    }

    "translate a query with a WHERE clause involving composite predicates" in {
      singleQueryExample(
        query = "SELECT a, b FROM c WHERE a = b AND b = a",
        expectedAst = Project(
          Filter(
            NamedTable("c", Map.empty, is_streaming = false),
            And(Equals(Id("a"), Id("b")), Equals(Id("b"), Id("a")))),
          Seq(simplyNamedColumn("a"), simplyNamedColumn("b"))))

      singleQueryExample(
        query = "SELECT a, b FROM c WHERE a = b OR b = a",
        expectedAst = Project(
          Filter(
            NamedTable("c", Map.empty, is_streaming = false),
            Or(Equals(Id("a"), Id("b")), Equals(Id("b"), Id("a")))),
          Seq(simplyNamedColumn("a"), simplyNamedColumn("b"))))

      singleQueryExample(
        query = "SELECT a, b FROM c WHERE NOT a = b",
        expectedAst = Project(
          Filter(NamedTable("c", Map.empty, is_streaming = false), Not(Equals(Id("a"), Id("b")))),
          Seq(simplyNamedColumn("a"), simplyNamedColumn("b"))))
    }

    "translate a query with a GROUP BY clause" in {
      singleQueryExample(
        query = "SELECT a, COUNT(b) FROM c GROUP BY a",
        expectedAst = Project(
          Aggregate(
            child = NamedTable("c", Map.empty, is_streaming = false),
            group_type = GroupBy,
            grouping_expressions = Seq(simplyNamedColumn("a")),
            pivot = None),
          Seq(simplyNamedColumn("a"), CallFunction("COUNT", Seq(Id("b"))))))
    }

    "translate a query with a GROUP BY and ORDER BY clauses" in {
      singleQueryExample(
        query = "SELECT a, COUNT(b) FROM c GROUP BY a ORDER BY a",
        expectedAst = Project(
          Sort(
            Aggregate(
              child = NamedTable("c", Map.empty, is_streaming = false),
              group_type = GroupBy,
              grouping_expressions = Seq(simplyNamedColumn("a")),
              pivot = None),
            Seq(SortOrder(Id("a"), Ascending, NullsLast)),
            is_global = false),
          Seq(simplyNamedColumn("a"), CallFunction("COUNT", Seq(Id("b"))))))
    }

    "translate a query with GROUP BY HAVING clause" in {
      singleQueryExample(
        query = "SELECT a, COUNT(b) FROM c GROUP BY a HAVING COUNT(b) > 1",
        expectedAst = Project(
          Filter(
            Aggregate(
              child = NamedTable("c", Map.empty, is_streaming = false),
              group_type = GroupBy,
              grouping_expressions = Seq(simplyNamedColumn("a")),
              pivot = None),
            GreaterThan(CallFunction("COUNT", Seq(Id("b"))), Literal(short = Some(1)))),
          Seq(simplyNamedColumn("a"), CallFunction("COUNT", Seq(Id("b"))))))
    }

    "translate a query with ORDER BY" in {
      singleQueryExample(
        query = "SELECT a FROM b ORDER BY a",
        expectedAst = Project(
          Sort(
            NamedTable("b", Map.empty, is_streaming = false),
            Seq(SortOrder(Id("a"), Ascending, NullsLast)),
            is_global = false),
          Seq(simplyNamedColumn("a"))))

      singleQueryExample(
        query = "SELECT a FROM b ORDER BY a DESC",
        expectedAst = Project(
          Sort(
            NamedTable("b", Map.empty, is_streaming = false),
            Seq(SortOrder(Id("a"), Descending, NullsFirst)),
            is_global = false),
          Seq(simplyNamedColumn("a"))))

      singleQueryExample(
        query = "SELECT a FROM b ORDER BY a NULLS FIRST",
        expectedAst = Project(
          Sort(
            NamedTable("b", Map.empty, is_streaming = false),
            Seq(SortOrder(Id("a"), Ascending, NullsFirst)),
            is_global = false),
          Seq(simplyNamedColumn("a"))))

      singleQueryExample(
        query = "SELECT a FROM b ORDER BY a DESC NULLS LAST",
        expectedAst = Project(
          Sort(
            NamedTable("b", Map.empty, is_streaming = false),
            Seq(SortOrder(Id("a"), Descending, NullsLast)),
            is_global = false),
          Seq(simplyNamedColumn("a"))))
    }

    "translate queries with LIMIT and OFFSET" in {
      singleQueryExample(
        query = "SELECT a FROM b LIMIT 5",
        expectedAst = Project(
          Limit(NamedTable("b", Map.empty, is_streaming = false), Literal(short = Some(5))),
          Seq(simplyNamedColumn("a"))))
      singleQueryExample(
        query = "SELECT a FROM b LIMIT 5 OFFSET 10",
        expectedAst = Project(
          Offset(
            Limit(NamedTable("b", Map.empty, is_streaming = false), Literal(short = Some(5))),
            Literal(short = Some(10))),
          Seq(simplyNamedColumn("a"))))
      singleQueryExample(
        query = "SELECT a FROM b OFFSET 10 FETCH FIRST 42",
        expectedAst = Project(
          Offset(NamedTable("b", Map.empty, is_streaming = false), Literal(short = Some(10))),
          Seq(simplyNamedColumn("a"))))
    }
    "translate a query with PIVOT" in {
      singleQueryExample(
        query = "SELECT a FROM b PIVOT (SUM(a) FOR c IN ('foo', 'bar'))",
        expectedAst = Project(
          Aggregate(
            child = NamedTable("b", Map.empty, is_streaming = false),
            group_type = Pivot,
            grouping_expressions = Seq(CallFunction("SUM", Seq(simplyNamedColumn("a")))),
            pivot =
              Some(Pivot(simplyNamedColumn("c"), Seq(Literal(string = Some("foo")), Literal(string = Some("bar")))))),
          Seq(simplyNamedColumn("a"))))
    }

    "translate a query with UNPIVOT" in {
      singleQueryExample(
        query = "SELECT a FROM b UNPIVOT (c FOR d IN (e, f))",
        expectedAst = Project(
          Unpivot(
            child = NamedTable("b", Map.empty, is_streaming = false),
            ids = Seq(simplyNamedColumn("e"), simplyNamedColumn("f")),
            values = None,
            variable_column_name = Id("c"),
            value_column_name = Id("d")),
          Seq(simplyNamedColumn("a"))))
    }

    "translate queries with WITH clauses" in {
      singleQueryExample(
        query = "WITH a (b, c, d) AS (SELECT x, y, z FROM e) SELECT b, c, d FROM a",
        expectedAst = WithCTE(
          Seq(
            CTEDefinition(
              tableName = "a",
              columns = Seq(simplyNamedColumn("b"), simplyNamedColumn("c"), simplyNamedColumn("d")),
              cte =
                Project(namedTable("e"), Seq(simplyNamedColumn("x"), simplyNamedColumn("y"), simplyNamedColumn("z"))))),
          Project(namedTable("a"), Seq(simplyNamedColumn("b"), simplyNamedColumn("c"), simplyNamedColumn("d")))))

      singleQueryExample(
        query =
          "WITH a (b, c, d) AS (SELECT x, y, z FROM e), aa (bb, cc) AS (SELECT xx, yy FROM f) SELECT b, c, d FROM a",
        expectedAst = WithCTE(
          Seq(
            CTEDefinition(
              tableName = "a",
              columns = Seq(simplyNamedColumn("b"), simplyNamedColumn("c"), simplyNamedColumn("d")),
              cte =
                Project(namedTable("e"), Seq(simplyNamedColumn("x"), simplyNamedColumn("y"), simplyNamedColumn("z")))),
            CTEDefinition(
              tableName = "aa",
              columns = Seq(simplyNamedColumn("bb"), simplyNamedColumn("cc")),
              cte = Project(namedTable("f"), Seq(simplyNamedColumn("xx"), simplyNamedColumn("yy"))))),
          Project(namedTable("a"), Seq(simplyNamedColumn("b"), simplyNamedColumn("c"), simplyNamedColumn("d")))))
    }

    "translate a query with WHERE, GROUP BY, HAVING, QUALIFY" in {
      singleQueryExample(
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
                child = Filter(namedTable("t1"), LessThan(Id("c3"), Literal(short = Some(4)))),
                group_type = GroupBy,
                grouping_expressions = Seq(simplyNamedColumn("c2"), simplyNamedColumn("c3")),
                pivot = None),
              GreaterThanOrEqual(CallFunction("AVG", Seq(Id("c1"))), Literal(short = Some(5)))),
            GreaterThan(CallFunction("MIN", Seq(Id("r"))), Literal(short = Some(6)))),
          Seq(
            simplyNamedColumn("c2"),
            Alias(Window(CallFunction("SUM", Seq(Id("c3"))), Seq(Id("c2")), Seq(), None), Seq(Id("r")), None))))
    }

    "translate a query with set operators" in {
      singleQueryExample(
        "SELECT a FROM t1 UNION SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(simplyNamedColumn("a"))),
          Project(namedTable("t2"), Seq(simplyNamedColumn("b"))),
          UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      singleQueryExample(
        "SELECT a FROM t1 UNION ALL SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(simplyNamedColumn("a"))),
          Project(namedTable("t2"), Seq(simplyNamedColumn("b"))),
          UnionSetOp,
          is_all = true,
          by_name = false,
          allow_missing_columns = false))
      singleQueryExample(
        "SELECT a FROM t1 MINUS SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(simplyNamedColumn("a"))),
          Project(namedTable("t2"), Seq(simplyNamedColumn("b"))),
          ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      singleQueryExample(
        "SELECT a FROM t1 EXCEPT SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(simplyNamedColumn("a"))),
          Project(namedTable("t2"), Seq(simplyNamedColumn("b"))),
          ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))

      singleQueryExample(
        "SELECT a FROM t1 INTERSECT SELECT b FROM t2",
        SetOperation(
          Project(namedTable("t1"), Seq(simplyNamedColumn("a"))),
          Project(namedTable("t2"), Seq(simplyNamedColumn("b"))),
          IntersectSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))

      singleQueryExample(
        "SELECT a FROM t1 INTERSECT SELECT b FROM t2 MINUS SELECT c FROM t3 UNION SELECT d FROM t4",
        SetOperation(
          SetOperation(
            SetOperation(
              Project(namedTable("t1"), Seq(simplyNamedColumn("a"))),
              Project(namedTable("t2"), Seq(simplyNamedColumn("b"))),
              IntersectSetOp,
              is_all = false,
              by_name = false,
              allow_missing_columns = false),
            Project(namedTable("t3"), Seq(simplyNamedColumn("c"))),
            ExceptSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          Project(namedTable("t4"), Seq(simplyNamedColumn("d"))),
          UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
    }

    "translate batches of queries" in {
      example(
        """
          |CREATE TABLE t1 (x VARCHAR);
          |SELECT x FROM t1;
          |SELECT 3 FROM t3;
          |""".stripMargin,
        _.snowflakeFile(),
        Batch(
          Seq(
            CreateTableCommand("t1", Seq(ColumnDeclaration("x", VarCharType(None)))),
            Project(namedTable("t1"), Seq(simplyNamedColumn("x"))),
            Project(namedTable("t3"), Seq(Literal(short = Some(3)))))))
    }

    // Tests below are just meant to verify that SnowflakeAstBuilder properly delegates DML commands
    // (other than SELECT) to SnowflakeDMLBuilder

    "translate INSERT commands" in {
      singleQueryExample(
        "INSERT INTO t (c1, c2, c3) VALUES (1,2, 3), (4, 5, 6)",
        InsertIntoTable(
          namedTable("t"),
          Some(Seq(Id("c1"), Id("c2"), Id("c3"))),
          Values(
            Seq(
              Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(short = Some(3))),
              Seq(Literal(short = Some(4)), Literal(short = Some(5)), Literal(short = Some(6))))),
          None,
          None,
          overwrite = false))
    }

    "translate DELETE commands" in {
      singleQueryExample(
        "DELETE FROM t WHERE t.c1 > 42",
        DeleteFromTable(
          namedTable("t"),
          None,
          Some(GreaterThan(Dot(Id("t"), Id("c1")), Literal(short = Some(42)))),
          None,
          None))

    }

    "translate UPDATE commands" in {
      singleQueryExample(
        "UPDATE t1 SET c1 = 42;",
        UpdateTable(namedTable("t1"), None, Seq(Assign(Id("c1"), Literal(short = Some(42)))), None, None, None))

    }
  }

}
