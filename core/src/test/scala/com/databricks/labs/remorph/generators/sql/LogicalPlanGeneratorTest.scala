package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.parsers.intermediate.{InnerJoin, JoinDataType, RightOuterJoin}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec

class LogicalPlanGeneratorTest extends AnyWordSpec with GeneratorTestCommon[ir.LogicalPlan] with ir.IRHelpers {

  override protected val generator = new LogicalPlanGenerator

  "Project" should {
    "transpile to SELECT" in {
      ir.Project(namedTable("t1"), Seq(ir.Id("c1"))) generates "SELECT c1 FROM t1"
      ir.Project(namedTable("t1"), Seq(ir.Star(None))) generates "SELECT * FROM t1"
      ir.Project(ir.NoTable(), Seq(ir.Literal(1))) generates "SELECT 1"
    }
  }

  "Filter" should {
    "transpile to WHERE" in {
      ir.Filter(
        ir.Project(namedTable("t1"), Seq(ir.Id("c1"))),
        ir.CallFunction("IS_DATE", Seq(ir.Id("c2")))) generates "SELECT c1 FROM t1 WHERE IS_DATE(c2)"
    }
  }

  "Join" should {
    "transpile to JOIN" in {
      crossJoin(namedTable("t1"), namedTable("t2")) generates "t1 JOIN t2"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        None,
        InnerJoin,
        Seq(),
        JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1 INNER JOIN t2"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        Some(ir.CallFunction("IS_DATE", Seq(ir.Id("c1")))),
        InnerJoin,
        Seq(),
        JoinDataType(is_left_struct = false, is_right_struct = false)) generates "t1 INNER JOIN t2 ON IS_DATE(c1)"

      ir.Join(
        namedTable("t1"),
        namedTable("t2"),
        Some(ir.CallFunction("IS_DATE", Seq(ir.Id("c1")))),
        RightOuterJoin,
        Seq("c1", "c2"),
        JoinDataType(
          is_left_struct = false,
          is_right_struct = false)) generates "t1 RIGHT OUTER JOIN t2 ON IS_DATE(c1) USING c1, c2"
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
}
