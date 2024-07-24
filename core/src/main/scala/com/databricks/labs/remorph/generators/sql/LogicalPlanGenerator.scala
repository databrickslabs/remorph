package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.transpilers.TranspileException

class LogicalPlanGenerator extends Generator[ir.LogicalPlan, String] {

  private val expressionGenerator = new ExpressionGenerator

  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): String = tree match {
    case b: ir.Batch => b.children.map(generate(ctx, _)).mkString("", ";\n", ";")
    case ir.WithCTE(ctes, query) =>
      s"WITH ${ctes.map(generate(ctx, _))} ${generate(ctx, query)}"
    case ir.Project(input, expressions) =>
      s"SELECT ${expressions.map(expressionGenerator.generate(ctx, _)).mkString(",")} FROM ${generate(ctx, input)}"
    case ir.NamedTable(id, _, _) => id
    case ir.Filter(input, condition) =>
      s"${generate(ctx, input)} WHERE ${expressionGenerator.generate(ctx, condition)}"
    case join: ir.Join => generateJoin(ctx, join)
    case x => throw TranspileException(s"not implemented ${x}")
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

    val conditionOpt = join.join_condition.map(expressionGenerator.generate(ctx, _))
    val spaceAndCondition = conditionOpt.map(" ON " + _).getOrElse("")
    val using = join.using_columns.mkString(", ")
    val spaceAndUsing = if (using.isEmpty) "" else s" USING $using"
    s"$left $joinType $right$spaceAndCondition$spaceAndUsing"
  }

}
