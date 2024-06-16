package com.databricks.labs.remorph.generators.sqlgen

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.intermediate.{Aggregate, And, Cast, Expression, Filter, Join, Limit, Plan, Project, Sort, SubqueryAlias, UnresolvedRelation, With}

import scala.util.matching.Regex

object SqlGenerator {
  def fromPlan(ctx: GeneratorContext, plan: Plan): String = plan match {
    case sa: SubqueryAlias =>
      subqueryPlan(ctx, sa)

    case w: With =>
      withPlan(ctx, w)

    case p: Project =>
      projectPlan(ctx, p)

    case Filter(condition, child) =>
      filterPlan(ctx, condition, child)

    case Limit(expr, child) =>
      limitPlan(ctx, expr, child)

    case Sort(order, global, child) =>
      sortPlan(ctx, order, child)

    case relation: UnresolvedRelation =>
      relationPlan(relation)

    case a: Aggregate =>
      aggregatePlan(ctx, a)

    case Join(left, right, joinType, condition, _) =>
      joinPlan(ctx, left, right, joinType, condition)

    case r: Range =>
      rangePlan(r)

    case Union(children, byName, allowMissingCol) =>
      unionPlan(ctx, children, byName, allowMissingCol)

    case LocalRelation(attrs, data, _) =>
      localRelationPlan(attrs, data)

    case _ =>
      throw new NotImplementedError(plan.toString())
  }

  private def subqueryPlan(ctx: GeneratorContext, sa: SubqueryAlias): String = sa match {
    case SubqueryAlias(identifier, _: LocalRelation) =>
      s"SELECT * FROM $identifier"
    case SubqueryAlias(identifier, nr: NamedRelation) =>
      s"SELECT * FROM $identifier AS ${nr.name}"
    case _ =>
      throw new NotImplementedError(s"not yet: $sa")
  }

  private def localRelationPlan(attrs: Seq[Attribute], data: Seq[InternalRow]) = {
    s"SELECT * FROM __LOCAL__"
  }

  private def unionPlan(ctx: GeneratorContext, children: Seq[Plan], byName: Boolean,
                        allowMissingCol: Boolean) = {
    if (byName) {
      val unionArg = if (allowMissingCol) ", allowMissingColumns=True" else ""
      // TODO: check
      children.map(fromPlan(ctx, _)).reduce((l, r) => s"($l)\nUNION ALL\n($r$unionArg)")
    }
    else children.map(fromPlan(ctx, _)).reduce((l, r) => s"($l)\nUNION\n($r)")
  }

  private def rangePlan(r: Range) = {
    s"spark.range(${r.start}, ${r.end}, ${r.step})"
  }

  private def joinPlan(ctx: GeneratorContext, left: Plan, right: Plan,
                       joinType: JoinType, condition: Option[Expression]) = {
    val (tp, on) = joinType match {
      case UsingJoin(tp, usingColumns) => (tp, usingColumns)
      case tp => (tp, Seq())
    }
    condition match {
      case Some(exp) =>
        s"""${fromPlan(ctx, left)}
           |${ctx.ws}${tp.sql} JOIN (${fromPlan(ctx, right)}) ${unfoldJoinCondition(ctx, exp)}
           |""".stripMargin
      case None =>
        s"""${fromPlan(ctx, left)}
           |${ctx.ws}${tp.sql} JOIN (${fromPlan(ctx, right)}) USING (${on.mkString(", ")})
           |""".stripMargin
    }
  }

  private def aggregatePlan(ctx: GeneratorContext, a: Aggregate) = {
    // matching against class name, as not all Spark implementations have compatible ABI
    val grpExprsRev = a.groupingExpressions.map(_.toString)
    // Removing col used for grouping from the agg expression
    val aggExprRev = a.aggregateExpressions.filter(item => !grpExprsRev.contains(item.toString))
    val aggs = SqlExpressions.smartDelimiters(ctx, aggExprRev.map(x => exprSql(ctx, x)))
    val groupBy = SqlExpressions.exprsSql(ctx, a.groupingExpressions)
    // TODO: refactor to With + CTE
    s"${fromPlan(ctx, a.child)}\n.groupBy($groupBy)\n.agg($aggs)"
  }

  private def relationPlan(relation: UnresolvedRelation) = {
    relation.name
  }

  private def sortPlan(ctx: GeneratorContext, order: Seq[SortOrder], child: Plan) = {
    val orderBy = order.map(item => {
      val dirStr = if (item.direction == Ascending) {
        "asc()"
      } else "desc()"
      item.child match {
        case Cast(colExpr, dataType, _) =>
          s"F.col(${q(SqlExpressions.exprSql(ctx, colExpr))})" +
            s".cast(${q(dataType.simpleString)}).$dirStr"
        case UnresolvedAttribute(nameParts) =>
          s"F.col(${q(nameParts.mkString("."))}).$dirStr"
      }
    })
    s"${fromPlan(ctx, child)}\n.orderBy(${orderBy.mkString(", ")})"
  }

  private def limitPlan(ctx: GeneratorContext, expr: Expression, child: Plan) = {
    s"${fromPlan(ctx, child)}\nLIMIT $expr"
  }

  private def filterPlan(ctx: GeneratorContext, condition: Expression, child: Plan) = {
    fromPlan(ctx, child) + s"\n${ctx.ws}WHERE " + unfoldWheres(ctx, condition)
  }

  private def withQueriesSql(ctx: GeneratorContext, withQueries: Seq[(String, SubqueryAlias)]) =
    withQueries map {
      case (str, SubqueryAlias(_, child)) =>
        val nest = ctx.nest
        s"$str AS (\n${nest.ws}${fromPlan(nest, child)}\n)"
    } mkString(",\n")

  private def withPlan(ctx: GeneratorContext, w: With): String = w match {
    case With(head, withQueries) =>
      s"WITH ${withQueriesSql(ctx, withQueries)}\n${fromPlan(ctx, head)}"
  }

  private def projectPlan(ctx: GeneratorContext, p: Project): String = p match {
      case Project(exprs, child) =>
        // TODO: this may break on FROM x AS y, but let's start with something
        val nest = ctx.nest
        s"SELECT ${exprsSql(nest, exprs)}\n${ctx.ws}FROM ${fromPlan(nest, child)}"
      case _ => throw new NotImplementedError(s"projection not yet implemented: $p")
    }

  private def unfoldJoinCondition(ctx: GeneratorContext, expr: Expression): String = expr match {
    case And(left, right) =>
      s"${unfoldJoinCondition(ctx, left)} && ${unfoldJoinCondition(ctx, right)}"
    case _ => s"${exprSql(ctx, expr)}"
  }

  private def unfoldWheres(ctx: GeneratorContext, expr: Expression): String = expr match {
    case And(left, right) =>
      s"${unfoldWheres(ctx, left)}\n${ctx.ws}AND ${unfoldWheres(ctx, right)}"
    case _ => s"${exprSql(ctx, expr)}"
  }

  private val pattern: Regex = "((?<![\\\\])['])".r

  /** Sugar for quoting strings */
  private def q(value: String) =
    if (pattern.findAllIn(value).toList.isEmpty) {
      "'" + value + "'"
    } else "\"" + value + "\""
}
