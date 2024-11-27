package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate.{Expression, _}

class DealiasLCAs extends Rule[LogicalPlan] with IRHelpers {

  override def apply(plan: LogicalPlan): LogicalPlan = {
    plan transform { case project: Project =>
      dealiasProject(project)
    }
  }

  private def dealiasProject(project: Project): Project = {
    val (dealiasedExpressions, aliases) =
      project.expressions.foldLeft((Seq.empty[Expression], Map.empty[String, Expression])) {
        case ((exprs, aliases), a: Alias) =>
          val dw = dealiasWindow(a.expr, aliases)
          (exprs :+ Alias(dw, a.name), aliases + (a.name.id -> dealiasExpression(dw, aliases)))
        case ((exprs, aliases), e) => (exprs :+ dealiasWindow(e, aliases), aliases)
      }

    val dealiasedInput = project.input transformDown { case Filter(in, cond) =>
      Filter(in, dealiasExpression(cond, aliases))
    }

    Project(dealiasedInput, dealiasedExpressions)

  }

  def dealiasWindow(expr: Expression, aliases: Map[String, Expression]): Expression = {
    expr transformDown { case w: Window =>
      w.mapChildren(dealiasExpression(_, aliases))
    }
  }

  def dealiasExpression(expr: Expression, aliases: Map[String, Expression]): Expression = {
    expr transformUp {
      case id: Id =>
        aliases.getOrElse(id.id, id)
      case e: Exists => Exists(apply(e.relation))
      case s: ScalarSubquery => ScalarSubquery(apply(s.plan))
    }
  }

}
