package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.{Parser, RuleContext}
import org.scalatest.wordspec.AnyWordSpec

trait SetOperationBehaviors[P <: Parser] extends ir.IRHelpers { this: ParserTestCommon[P] with AnyWordSpec =>

  def setOperationsAreTranslated[R <: RuleContext](rule: P => R): Unit = {
    def testSimpleExample(query: String, expectedAst: LogicalPlan): Unit = {
      query in {
        example(query, rule, expectedAst)
      }
    }

    "translate set operations" should {
      /* These are of the form:
       *   SELECT [...] ((UNION [ALL] | EXCEPT | INTERSECT) SELECT [...])*
       *
       * Note that precedence is:
       *  1. Brackets.
       *  2. INTERSECT
       *  3. UNION and EXCEPT, from left to right.
       */
      testSimpleExample(
        "SELECT 1 UNION SELECT 2",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
          ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
          ir.UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "SELECT 1 UNION ALL SELECT 2",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
          ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
          ir.UnionSetOp,
          is_all = true,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "SELECT 1 EXCEPT SELECT 2",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
          ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
          ir.ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "SELECT 1 INTERSECT SELECT 2",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
          ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
          ir.IntersectSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "SELECT 1 UNION SELECT 2 UNION ALL SELECT 3 EXCEPT SELECT 4 INTERSECT SELECT 5",
        ir.SetOperation(
          ir.SetOperation(
            ir.SetOperation(
              ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
              ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
              ir.UnionSetOp,
              is_all = false,
              by_name = false,
              allow_missing_columns = false),
            ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType))),
            ir.UnionSetOp,
            is_all = true,
            by_name = false,
            allow_missing_columns = false),
          ir.SetOperation(
            ir.Project(ir.NoTable, Seq(ir.Literal(4, ir.IntegerType))),
            ir.Project(ir.NoTable, Seq(ir.Literal(5, ir.IntegerType))),
            ir.IntersectSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          ir.ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      // Part of checking that UNION and EXCEPT are processed with the same precedence: left-to-right
      testSimpleExample(
        "SELECT 1 UNION SELECT 2 EXCEPT SELECT 3",
        ir.SetOperation(
          ir.SetOperation(
            ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
            ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
            ir.UnionSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType))),
          ir.ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      // Part of checking that UNION and EXCEPT are processed with the same precedence: left-to-right
      testSimpleExample(
        "SELECT 1 EXCEPT SELECT 2 UNION SELECT 3",
        ir.SetOperation(
          ir.SetOperation(
            ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
            ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
            ir.ExceptSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType))),
          ir.UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      // INTERSECT has higher precedence than both UNION and EXCEPT
      testSimpleExample(
        "SELECT 1 UNION SELECT 2 EXCEPT SELECT 3 INTERSECT SELECT 4",
        ir.SetOperation(
          ir.SetOperation(
            ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
            ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
            ir.UnionSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          ir.SetOperation(
            ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType))),
            ir.Project(ir.NoTable, Seq(ir.Literal(4, ir.IntegerType))),
            ir.IntersectSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          ir.ExceptSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "SELECT 1 UNION (SELECT 2 UNION ALL SELECT 3) INTERSECT (SELECT 4 EXCEPT SELECT 5)",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType))),
          ir.SetOperation(
            ir.SetOperation(
              ir.Project(ir.NoTable, Seq(ir.Literal(2, ir.IntegerType))),
              ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType))),
              ir.UnionSetOp,
              is_all = true,
              by_name = false,
              allow_missing_columns = false),
            ir.SetOperation(
              ir.Project(ir.NoTable, Seq(ir.Literal(4, ir.IntegerType))),
              ir.Project(ir.NoTable, Seq(ir.Literal(5, ir.IntegerType))),
              ir.ExceptSetOp,
              is_all = false,
              by_name = false,
              allow_missing_columns = false),
            ir.IntersectSetOp,
            is_all = false,
            by_name = false,
            allow_missing_columns = false),
          ir.UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "(SELECT 1, 2) UNION SELECT 3, 4",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType), ir.Literal(2, ir.IntegerType))),
          ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType), ir.Literal(4, ir.IntegerType))),
          ir.UnionSetOp,
          is_all = false,
          by_name = false,
          allow_missing_columns = false))
      testSimpleExample(
        "(SELECT 1, 2) UNION ALL SELECT 3, 4",
        ir.SetOperation(
          ir.Project(ir.NoTable, Seq(ir.Literal(1, ir.IntegerType), ir.Literal(2, ir.IntegerType))),
          ir.Project(ir.NoTable, Seq(ir.Literal(3, ir.IntegerType), ir.Literal(4, ir.IntegerType))),
          ir.UnionSetOp,
          is_all = true,
          by_name = false,
          allow_missing_columns = false))
    }
  }
}
