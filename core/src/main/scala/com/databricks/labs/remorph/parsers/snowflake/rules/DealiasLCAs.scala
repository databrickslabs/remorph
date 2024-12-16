package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors}
import com.databricks.labs.remorph.intermediate.{Expression, _}

class DealiasLCAs extends Rule[LogicalPlan] with IRHelpers with TransformationConstructors {

  override def apply(plan: LogicalPlan): Transformation[LogicalPlan] = transformPlan(plan)

  private[rules] def transformPlan(plan: LogicalPlan): Transformation[LogicalPlan] =
    plan transform { case project: Project =>
      dealiasProject(project)
    }

  private def dealiasProject(project: Project): Transformation[Project] = {
    // Go through the Project's select list, collecting aliases
    // and dealias expressions using the aliases collected thus far
    val init = ok((Map.empty[String, Expression], Seq.empty[Expression]))
    project.expressions
      .foldLeft(init) {
        case (transfo, a @ Alias(expr, name)) =>
          transfo.flatMap { case (aliases, exprs) =>
            // LCA aren't supported in WINDOW clauses, so we must dealias them
            dealiasWindow(expr, aliases).flatMap { dw =>
              val accumulatedExprs = exprs :+ CurrentOrigin.withOrigin(a.origin)(Alias(dw, name))
              // An aliased expression may refer to a previous LCA, so before storing the mapping,
              // we must dealias the expression to ensure that mapped expressions are fully dealiased.
              dealiasExpression(dw, aliases).map { newFoundAlias =>
                val updatedAliases = aliases + (name.id -> newFoundAlias)
                (updatedAliases, accumulatedExprs)
              }
            }
          }
        case (transfo, e) =>
          transfo.flatMap { case (aliases, exprs) =>
            dealiasWindow(e, aliases).map(dw => (aliases, exprs :+ dw))
          }

      }
      .flatMap { case (aliases, dealiasedExpressions) =>
        project.input
          .transformDown { case f @ Filter(in, cond) =>
            dealiasExpression(cond, aliases).map { dealiasedCond =>
              CurrentOrigin.withOrigin(f.origin)(Filter(in, dealiasedCond))
            }
          }
          .map { dealiasedInput =>
            CurrentOrigin.withOrigin(project.origin)(Project(dealiasedInput, dealiasedExpressions))
          }
      }

  }

  private def dealiasWindow(expr: Expression, aliases: Map[String, Expression]): Transformation[Expression] = {
    expr transformDown { case w: Window =>
      w.mapChildren(dealiasExpression(_, aliases))
    }
  }

  private def dealiasExpression(expr: Expression, aliases: Map[String, Expression]): Transformation[Expression] = {
    expr transformUp {
      case id: Id => ok(aliases.getOrElse(id.id, id))
      case n: Name => ok(aliases.getOrElse(n.name, n))
      case e: Exists => transformPlan(e.relation).map(plan => CurrentOrigin.withOrigin(e.origin)(Exists(plan)))
      case s: ScalarSubquery =>
        transformPlan(s.plan).map(plan => CurrentOrigin.withOrigin(s.origin)(ScalarSubquery(plan)))
    }
  }

}
