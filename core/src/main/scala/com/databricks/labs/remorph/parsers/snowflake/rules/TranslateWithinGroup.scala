package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate.UnresolvedNamedLambdaVariable
import com.databricks.labs.remorph.{intermediate => ir}

import scala.annotation.tailrec

class TranslateWithinGroup extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): ir.LogicalPlan = {
    plan transformAllExpressions {
      case ir.WithinGroup(ir.CallFunction("ARRAY_AGG", args), sorts) => sortArray(args.head, sorts)
      case ir.WithinGroup(ir.CallFunction("LISTAGG", args), sorts) =>
        ir.ArrayJoin(sortArray(args.head, sorts), args(1))
    }
  }

  private def sortArray(arg: ir.Expression, sort: Seq[ir.SortOrder]): ir.Expression = {
    if (sort.size == 1 && sameReference(arg, sort.head.expr)) {
      val sortOrder = if (sort.head.direction == ir.Descending) { Some(ir.Literal(false)) }
      else { None }
      ir.SortArray(ir.CollectList(arg), sortOrder)
    } else {

      val namedStructFunc = ir.CreateNamedStruct(Seq(ir.Literal("value"), arg) ++ sort.zipWithIndex.flatMap {
        case (s, index) =>
          Seq(ir.Literal(s"sort_by_$index"), s.expr)
      })

      ir.ArrayTransform(
        ir.ArraySort(ir.CollectList(namedStructFunc), sortingLambda(sort)),
        ir.LambdaFunction(ir.Dot(ir.Id("s"), ir.Id("value")), Seq(ir.UnresolvedNamedLambdaVariable(Seq("s")))))
    }
  }

  @tailrec private def sameReference(left: ir.Expression, right: ir.Expression): Boolean = left match {
    case ir.Distinct(e) => sameReference(e, right)
    case l if l == right => true
    case _ => false
  }

  private def sortingLambda(sort: Seq[ir.SortOrder]): ir.Expression = {
    ir.LambdaFunction(
      ir.Case(
        None,
        sort.zipWithIndex.flatMap { case (s, index) =>
          Seq(
            ir.WhenBranch(
              ir.LessThan(
                ir.Dot(ir.Id("left"), ir.Id(s"sort_by_$index")),
                ir.Dot(ir.Id("right"), ir.Id(s"sort_by_$index"))),
              if (s.direction == ir.Ascending) ir.Literal(-1) else ir.Literal(1)),
            ir.WhenBranch(
              ir.GreaterThan(
                ir.Dot(ir.Id("left"), ir.Id(s"sort_by_$index")),
                ir.Dot(ir.Id("right"), ir.Id(s"sort_by_$index"))),
              if (s.direction == ir.Ascending) ir.Literal(1) else ir.Literal(-1)))
        },
        Some(ir.Literal(0))),
      Seq(UnresolvedNamedLambdaVariable(Seq("left")), UnresolvedNamedLambdaVariable(Seq("right"))))
  }
}
