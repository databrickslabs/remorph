package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py

object PySparkStatements {
  def apply(plan: ir.LogicalPlan): py.Module = plan match {
    case ir.Batch(children) =>
      val statements = children.map(Action)
      py.Module(statements)
  }
}

case class Action(plan: ir.LogicalPlan) extends py.LeafStatement

class PySparkStatements(val expr: ir.Rule[ir.Expression]) extends ir.Rule[py.Statement] with PyCommon {
  override def apply(in: py.Statement): py.Statement = in match {
    case py.Module(statements) => py.Module(statements.map(apply))
    case Action(logical) => py.ExprStatement(plan(pythonize(logical)))
  }

  private def pythonize(logical: ir.LogicalPlan): ir.LogicalPlan = {
    logical transformExpressionsDown { case e: ir.Expression =>
      expr(e)
    }
  }

  private def plan(logical: ir.LogicalPlan): ir.Expression = logical match {
    case ir.PlanComment(input, text) => py.Comment(plan(input), text)
    case ir.NamedTable(name, _, _) => methodOf(ir.Name("spark"), "table", Seq(ir.StringLiteral(name)))
    case ir.NoTable => methodOf(ir.Name("spark"), "emptyDataFrame", Seq())
    case ir.Filter(input, condition) => methodOf(plan(input), "filter", Seq(condition))
    case ir.Project(input, projectList) => methodOf(plan(input), "select", projectList)
    case ir.Limit(input, limit) => methodOf(plan(input), "limit", Seq(limit))
    case ir.Offset(input, offset) => methodOf(plan(input), "offset", Seq(offset))
    case ir.Sort(input, sortList, _) => methodOf(plan(input), "orderBy", sortList)
    case ir.Aggregate(input, ir.GroupBy, exprs, _) => methodOf(plan(input), "groupBy", exprs)
    case ir.Deduplicate(input, keys, _, _) => methodOf(plan(input), "dropDuplicates", keys)
  }
}
