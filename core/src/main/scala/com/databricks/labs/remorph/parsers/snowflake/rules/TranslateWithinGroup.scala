package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.UnresolvedNamedLambdaVariable
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.annotation.tailrec

class TranslateWithinGroup extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): ir.LogicalPlan = {
    plan transformAllExpressions {
      case ir.WithinGroup(ir.CallFunction("ARRAY_AGG", args), sorts) => sortArray(args.head, sorts.head)
      case ir.WithinGroup(ir.CallFunction("LISTAGG", args), sorts) =>
        ir.ArrayJoin(sortArray(args.head, sorts.head), args(1))
    }
  }

  private def sortArray(arg: ir.Expression, sort: ir.SortOrder): ir.Expression = {
    if (sameReference(arg, sort.expr)) {
      val sortOrder = if (sort.direction == ir.Descending) { Some(ir.Literal(false)) }
      else { None }
      ir.SortArray(ir.CollectList(arg), sortOrder)
    } else {

      ir.ArrayTransform(
        ir.ArraySort(
          ir.CollectList(ir.CreateNamedStruct(Seq(ir.Literal("value"), arg, ir.Literal("sort_by"), sort.expr))),
          sortingLambda(sort.direction)),
        ir.LambdaFunction(ir.Dot(ir.Id("s"), ir.Id("value")), Seq(ir.UnresolvedNamedLambdaVariable(Seq("s")))))
    }
  }

  @tailrec private def sameReference(left: ir.Expression, right: ir.Expression): Boolean = left match {
    case ir.Distinct(e) => sameReference(e, right)
    case l if l == right => true
    case _ => false
  }

  private def sortingLambda(dir: ir.SortDirection): ir.Expression = {
    ir.LambdaFunction(
      ir.Case(
        None,
        Seq(
          ir.WhenBranch(
            ir.LessThan(ir.Dot(ir.Id("left"), ir.Id("sort_by")), ir.Dot(ir.Id("right"), ir.Id("sort_by"))),
            if (dir == ir.Ascending) ir.Literal(-1) else ir.Literal(1)),
          ir.WhenBranch(
            ir.GreaterThan(ir.Dot(ir.Id("left"), ir.Id("sort_by")), ir.Dot(ir.Id("right"), ir.Id("sort_by"))),
            if (dir == ir.Ascending) ir.Literal(1) else ir.Literal(-1))),
        Some(ir.Literal(0))),
      Seq(UnresolvedNamedLambdaVariable(Seq("left")), UnresolvedNamedLambdaVariable(Seq("right"))))
  }
}
