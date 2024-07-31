package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.parsers.intermediate.{ExceptSetOp, IntersectSetOp, MergeIntoTable, UnionSetOp}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

class LogicalPlanGenerator(val expr: ExpressionGenerator, val explicitDistinct: Boolean = false)
    extends Generator[ir.LogicalPlan, String] {

  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): String = tree match {
    case b: ir.Batch => b.children.map(generate(ctx, _)).mkString("", ";\n", ";")
    case ir.WithCTE(ctes, query) =>
      s"WITH ${ctes.map(generate(ctx, _))} ${generate(ctx, query)}"
    case p: ir.Project => project(ctx, p)
    case ir.NamedTable(id, _, _) => id
    case ir.Filter(input, condition) =>
      s"${generate(ctx, input)} WHERE ${expr.generate(ctx, condition)}"
    case ir.Limit(input, limit) =>
      s"${generate(ctx, input)} LIMIT ${expr.generate(ctx, limit)}"
    case ir.Offset(child, offset) =>
      s"${generate(ctx, child)} OFFSET ${expr.generate(ctx, offset)}"
    case ir.Values(data) =>
      s"VALUES ${data.map(_.map(expr.generate(ctx, _)).mkString("(", ",", ")")).mkString(", ")}"
    case agg: ir.Aggregate => aggregate(ctx, agg)
    case sort: ir.Sort => orderBy(ctx, sort)
    case join: ir.Join => generateJoin(ctx, join)
    case setOp: ir.SetOperation => setOperation(ctx, setOp)
    case mergeIntoTable: ir.MergeIntoTable => generateMerge(ctx, mergeIntoTable)
    case withOptions: ir.WithOptions => generateWithOptions(ctx, withOptions)
    case x => throw unknown(x)
  }

  private def project(ctx: GeneratorContext, proj: ir.Project): String = {
    val fromClause = if (proj.input != ir.NoTable()) {
      s" FROM ${generate(ctx, proj.input)}"
    } else {
      ""
    }
    s"SELECT ${proj.expressions.map(expr.generate(ctx, _)).mkString(",")}$fromClause"
  }

  private def orderBy(ctx: GeneratorContext, sort: ir.Sort): String = {
    val orderStr = sort.order
      .map { case ir.SortOrder(child, direction, nulls) =>
        s"${expr.generate(ctx, child)} ${direction.sql} ${nulls.sql}"
      }
      .mkString(", ")
    s"${generate(ctx, sort.child)} ORDER BY $orderStr"
  }

  private def generateJoin(ctx: GeneratorContext, join: ir.Join): String = {
    val left = generate(ctx, join.left)
    val right = generate(ctx, join.right)
    val joinType = join.join_type match {
      case ir.InnerJoin => "INNER JOIN"
      case ir.FullOuterJoin => "FULL OUTER JOIN"
      case ir.LeftOuterJoin => "LEFT OUTER JOIN"
      case ir.LeftSemiJoin => "LEFT SEMI JOIN"
      case ir.LeftAntiJoin => "LEFT ANTI JOIN"
      case ir.RightOuterJoin => "RIGHT OUTER JOIN"
      case ir.CrossJoin => "JOIN"
    }

    val conditionOpt = join.join_condition.map(expr.generate(ctx, _))
    val spaceAndCondition = conditionOpt.map(" ON " + _).getOrElse("")
    val using = join.using_columns.mkString(", ")
    val spaceAndUsing = if (using.isEmpty) "" else s" USING ($using)"
    s"$left $joinType $right$spaceAndCondition$spaceAndUsing"
  }

  private def setOperation(ctx: GeneratorContext, setOp: ir.SetOperation): String = {
    if (setOp.allow_missing_columns) {
      throw unknown(setOp)
    }
    if (setOp.by_name) {
      throw unknown(setOp)
    }
    val op = setOp.set_op_type match {
      case UnionSetOp => "UNION"
      case IntersectSetOp => "INTERSECT"
      case ExceptSetOp => "EXCEPT"
      case _ => throw unknown(setOp)
    }
    val duplicates = if (setOp.is_all) " ALL" else if (explicitDistinct) " DISTINCT" else ""
    s"(${generate(ctx, setOp.left)}) $op$duplicates (${generate(ctx, setOp.right)})"
  }

  private def generateMerge(ctx: GeneratorContext, mergeIntoTable: MergeIntoTable) = {
    val target = generate(ctx, mergeIntoTable.targetTable)
    val source = generate(ctx, mergeIntoTable.sourceTable)
    val condition = expr.generate(ctx, mergeIntoTable.mergeCondition)

    val matchedActions = mergeIntoTable.matchedActions
      .map { action =>
        val conditionText = action.condition.map(cond => s" AND ${expr.generate(ctx, cond)}").getOrElse("")
        s" WHEN MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }
      .mkString("")

    val notMatchedActions = mergeIntoTable.notMatchedActions
      .map { action =>
        val conditionText = action.condition.map(cond => s" AND ${expr.generate(ctx, cond)}").getOrElse("")
        s" WHEN NOT MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }
      .mkString("")

    val notMatchedBySourceActions = mergeIntoTable.notMatchedBySourceActions
      .map { action =>
        val conditionText = action.condition.map(cond => s" AND ${expr.generate(ctx, cond)}").getOrElse("")
        s" WHEN NOT MATCHED BY SOURCE${conditionText} THEN ${expr.generate(ctx, action)}"
      }
      .mkString("")

    s"MERGE INTO $target" +
      s" USING $source" +
      s" ON ${condition}" +
      s"${matchedActions}" +
      s"${notMatchedActions}" +
      s"${notMatchedBySourceActions};"
  }

  private def aggregate(ctx: GeneratorContext, aggregate: ir.Aggregate): String = {
    val child = generate(ctx, aggregate.child)
    val expressions = aggregate.grouping_expressions.map(expr.generate(ctx, _)).mkString(", ")
    aggregate.group_type match {
      case ir.GroupBy =>
        s"$child GROUP BY $expressions"
      case ir.Pivot if aggregate.pivot.isDefined =>
        val pivot = aggregate.pivot.get
        val col = expr.generate(ctx, pivot.col)
        val values = pivot.values.map(expr.generate(ctx, _)).mkString(" IN(", ", ", ")")
        s"$child PIVOT($expressions FOR $col$values)"
      case a => throw TranspileException(s"Unsupported aggregate $a")
    }
  }
  private def generateWithOptions(ctx: GeneratorContext, withOptions: ir.WithOptions): String = {
    val optionComments = expr.generate(ctx, withOptions.options)
    val plan = generate(ctx, withOptions.input)
    s"${optionComments}" +
      s"${plan}"
  }
}
