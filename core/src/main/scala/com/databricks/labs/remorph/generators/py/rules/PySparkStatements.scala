package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py

object PySparkStatements {
  def apply(batch: ir.Batch): py.Module = {
    val statements = batch.children.map(Action)
    py.Module(statements)
  }
}

case class Action(plan: ir.LogicalPlan) extends py.LeafStatement

class PySparkStatements(val expr: PySparkExpressions) extends ir.Rule[py.Statement] with PyCommon {
  override def apply(in: py.Statement): py.Statement = in match {
    case Action(logical) => py.ExprStatement(plan(logical))
  }

  private def plan(logical: ir.LogicalPlan): ir.Expression = logical match {
    case ir.NoTable() => methodOf(ir.Name("spark"), "emptyDataFrame", Seq())
    case ir.Filter(input, condition) => methodOf(plan(input), "filter", Seq(expr.apply(condition)))
    case ir.Project(input, projectList) => methodOf(plan(input), "select", projectList.map(expr.apply))
    case ir.Limit(input, limit) => methodOf(plan(input), "limit", Seq(expr.apply(limit)))
    case ir.Offset(input, offset) => methodOf(plan(input), "offset", Seq(expr.apply(offset)))
    case ir.Sort(input, sortList, _) => methodOf(plan(input), "orderBy", sortList.map(expr.apply))
    case ir.Aggregate(input, ir.GroupBy, exprs, _) => methodOf(plan(input), "groupBy", exprs.map(expr.apply))
    case ir.Deduplicate(input, keys, _, _) => methodOf(plan(input), "dropDuplicates", keys.map(expr.apply))
  }
}