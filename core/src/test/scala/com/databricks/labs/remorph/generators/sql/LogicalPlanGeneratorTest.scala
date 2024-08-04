package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec

class LogicalPlanGeneratorTest extends AnyWordSpec with GeneratorTestCommon[ir.LogicalPlan] with ir.IRHelpers {

  override protected val generator = new LogicalPlanGenerator(new ExpressionGenerator())

  "Project" should {
    "transpile to SELECT" in {
      ir.Project(namedTable("t1"), Seq(ir.Id("c1"))) generates "SELECT c1 FROM t1"
      ir.Project(namedTable("t1"), Seq(ir.Star(None))) generates "SELECT * FROM t1"
      ir.Project(ir.NoTable(), Seq(ir.Literal(1))) generates "SELECT 1"
    }

    "transpile to SELECT with COMMENTS" in {
      ir.WithOptions(
        ir.Project(namedTable("t"), Seq(ir.Star(None))),
        ir.Options(
          Map(
            "MAXRECURSION" -> ir.Literal(short = Some(10)),
            "OPTIMIZE" -> ir.Column(None, ir.Id("FOR", caseSensitive = true))),
          Map("SOMESTROPT" -> "STRINGOPTION"),
          Map("SOMETHING" -> true, "SOMETHINGELSE" -> false),
          List("SOMEOTHER"))) generates
        """/*
            |   The following statement was originally given the following OPTIONS:
            |
            |    Expression options:
            |
            |     MAXRECURSION = 10
            |     OPTIMIZE = "FOR"
            |
            |    String options:
            |
            |     SOMESTROPT = 'STRINGOPTION'
            |
            |    Boolean options:
            |
            |     SOMETHING ON
            |     SOMETHINGELSE OFF
            |
            |    Auto options:
            |
            |     SOMEOTHER AUTO
            |
            |
            | */
            |SELECT * FROM t""".stripMargin
    }
  }

  "Filter" should {
    "transpile to WHERE" in {
      ir.Filter(
        ir.Project(namedTable("t1"), Seq(ir.Id("c1"))),
        ir.CallFunction("IS_DATE", Seq(ir.Id("c2")))) generates "SELECT c1 FROM t1 WHERE IS_DATE(c2)"
    }
  }

  "MergeIntoTable" should {
    "transpile to MERGE" in {
      ir.MergeIntoTable(
        namedTable("t"),
        namedTable("s"),
        ir.Equals(
          ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("a")),
          ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
        Seq(
          ir.UpdateAction(
            None,
            Seq(
              ir.Assign(
                ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("b")),
                ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b"))))),
          ir.DeleteAction(
            Some(ir.LessThan(ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")), ir.Literal(10))))),
        Seq(
          ir.InsertAction(
            None,
            Seq(
              ir.Assign(ir.Column(None, ir.Id("a")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
              ir.Assign(ir.Column(None, ir.Id("b")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")))))),
        List.empty) generates
        "MERGE INTO t USING s ON t.a = s.a" +
        " WHEN MATCHED THEN UPDATE SET t.b = s.b" +
        " WHEN MATCHED AND s.b < 10 THEN DELETE" +
        " WHEN NOT MATCHED THEN INSERT (a, b) VALUES (s.a, s.b)" +
        ";"
    }
    "transpile to MERGE with comments" in {
      ir.WithOptions(
        ir.MergeIntoTable(
          ir.NamedTable("t", Map(), is_streaming = false),
          ir.NamedTable("s", Map(), is_streaming = false),
          ir.Equals(
            ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("a")),
            ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
          Seq(
            ir.UpdateAction(
              None,
              Seq(
                ir.Assign(
                  ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("b")),
                  ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")))))),
          Seq(
            ir.InsertAction(
              None,
              Seq(
                ir.Assign(ir.Column(None, ir.Id("a")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("a"))),
                ir.Assign(ir.Column(None, ir.Id("b")), ir.Column(Some(ir.ObjectReference(ir.Id("s"))), ir.Id("b")))))),
          List.empty),
        ir.Options(
          Map(
            "KEEPFIXED" -> ir.Column(None, ir.Id("PLAN")),
            "FAST" -> ir.Literal(short = Some(666)),
            "MAX_GRANT_PERCENT" -> ir.Literal(short = Some(30))),
          Map(),
          Map("FLAME" -> false, "QUICKLY" -> true),
          List())) generates
        """/*
          |   The following statement was originally given the following OPTIONS:
          |
          |    Expression options:
          |
          |     KEEPFIXED = PLAN
          |     FAST = 666
          |     MAX_GRANT_PERCENT = 30
          |
          |    Boolean options:
          |
          |     FLAME OFF
          |     QUICKLY ON
          |
          |
          | */
          |""".stripMargin +
        "MERGE INTO t USING s ON t.a = s.a" +
        " WHEN MATCHED THEN UPDATE SET t.b = s.b" +
        " WHEN NOT MATCHED THEN INSERT (a, b) VALUES (s.a, s.b)" +
        ";"
    }
  }

  "Join" should {
    "transpile to JOIN" in {
      crossJoin(namedTable("t1"), namedTable("t2")) generates "t1 JOIN t2"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        None,
        ir.InnerJoin,
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1 INNER JOIN t2"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        Some(ir.CallFunction("IS_DATE", Seq(ir.Id("c1")))),
        ir.InnerJoin,
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1 INNER JOIN t2 ON IS_DATE(c1)"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        Some(ir.CallFunction("IS_DATE", Seq(ir.Id("c1")))),
        ir.RightOuterJoin,
        Seq("c1", "c2"),
        ir.JoinDataType(
          is_left_struct = false,
          is_right_struct = false)) generates "t1 RIGHT OUTER JOIN t2 ON IS_DATE(c1) USING (c1, c2)"
    }
  }

  "SetOperation" should {
    "transpile to UNION" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnionSetOp,
        is_all = false,
        by_name = false,
        allow_missing_columns = false) generates "(a) UNION (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnionSetOp,
        is_all = true,
        by_name = false,
        allow_missing_columns = false) generates "(a) UNION ALL (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnionSetOp,
        is_all = true,
        by_name = true,
        allow_missing_columns = false)
        .doesNotTranspile
    }

    "transpile to INTERSECT" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.IntersectSetOp,
        is_all = false,
        by_name = false,
        allow_missing_columns = false) generates "(a) INTERSECT (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.IntersectSetOp,
        is_all = true,
        by_name = false,
        allow_missing_columns = false) generates "(a) INTERSECT ALL (b)"
    }

    "transpile to EXCEPT" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.ExceptSetOp,
        is_all = false,
        by_name = false,
        allow_missing_columns = false) generates "(a) EXCEPT (b)"
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.ExceptSetOp,
        is_all = true,
        by_name = false,
        allow_missing_columns = false) generates "(a) EXCEPT ALL (b)"
    }

    "unspecified" in {
      ir.SetOperation(
        namedTable("a"),
        namedTable("b"),
        ir.UnspecifiedSetOp,
        is_all = true,
        by_name = true,
        allow_missing_columns = false)
        .doesNotTranspile
    }
  }

  "transpile to LIMIT" in {
    ir.Limit(namedTable("a"), ir.Literal(10)) generates "a LIMIT 10"
  }

  "transpile to OFFSET" in {
    ir.Offset(namedTable("a"), ir.Literal(10)) generates "a OFFSET 10"
  }

  "transpile to ORDER BY" in {
    ir.Sort(
      namedTable("a"),
      Seq(ir.SortOrder(ir.Id("c1"), ir.Ascending, ir.NullsFirst))) generates "a ORDER BY c1 ASC NULLS FIRST"
  }

  "transpile to VALUES" in {
    ir.Values(Seq(Seq(ir.Literal(1), ir.Literal(2)), Seq(ir.Literal(3), ir.Literal(4)))) generates "VALUES (1,2), (3,4)"
  }

  "Aggregate" should {
    "transpile to GROUP BY" in {
      ir.Aggregate(namedTable("t1"), ir.GroupBy, Seq(ir.Id("c1")), None) generates "t1 GROUP BY c1"
    }

    "transpile to PIVOT" in {
      ir.Aggregate(
        namedTable("t1"),
        ir.Pivot,
        Seq(ir.Id("c1")),
        Some(ir.Pivot(ir.Id("c2"), Seq(ir.Literal(1), ir.Literal(2))))) generates
        "t1 PIVOT(c1 FOR c2 IN(1, 2))"
    }

  }
}
