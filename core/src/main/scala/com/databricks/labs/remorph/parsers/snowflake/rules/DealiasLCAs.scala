package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate.{Expression, _}

class DealiasLCAs extends Rule[LogicalPlan] with IRHelpers {

  override def apply(plan: LogicalPlan): LogicalPlan = transformPlan(plan)

  private def transformPlan(plan: LogicalPlan): LogicalPlan =
    plan transform { case project: Project =>
      dealiasProject(project)
    }

  private def dealiasProject(project: Project): Project = {
    // Go through the Project's select list, collecting aliases
    // and dealias expressions using the aliases collected thus far
    val (aliases, dealiasedExpressions) =
      project.expressions.foldLeft((Map.empty[String, Expression], Seq.empty[Expression])) {
        case ((aliases, exprs), Alias(expr, name)) =>
          // LCA aren't supported in WINDOW clauses, so we must dealias them
          val dw = dealiasWindow(expr, aliases)
          val accumulatedExprs = exprs :+ Alias(dw, name)
          // An aliased expression may refer to an previous LCA, so before storing the mapping,
          // we must dealias the expression to ensure that mapped expressions are fully dealiased.
          val newFoundAlias = dealiasExpression(dw, aliases)
          val updatedAliases = aliases + (name.id -> newFoundAlias)
          (updatedAliases, accumulatedExprs)
        case ((aliases, exprs), e) => (aliases, exprs :+ dealiasWindow(e, aliases))
      }

    val dealiasedInput = project.input transformDown { case Filter(in, cond) =>
      Filter(in, dealiasExpression(cond, aliases))
    }

    Project(dealiasedInput, dealiasedExpressions)
  }

  private def dealiasWindow(expr: Expression, aliases: Map[String, Expression]): Expression = {
    expr transformDown { case w: Window =>
      w.mapChildren(dealiasExpression(_, aliases))
    }
  }

  private def dealiasExpression(expr: Expression, aliases: Map[String, Expression]): Expression = {
    expr transformUp {
      case id: Id => aliases.getOrElse(id.id, id)
      case n: Name => aliases.getOrElse(n.name, n)
      case e: Exists => Exists(transformPlan(e.relation))
      case s: ScalarSubquery => ScalarSubquery(transformPlan(s.plan))
    }
  }

}
