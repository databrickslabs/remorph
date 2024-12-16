package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.{Optimizing, PartialResult, Transformation, TransformationConstructors, WorkflowStage}
import com.databricks.labs.remorph.intermediate._

case class TopPercent(child: LogicalPlan, percentage: Expression, with_ties: Boolean = false) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

class TopPercentToLimitSubquery extends Rule[LogicalPlan] with TransformationConstructors {
  override def apply(plan: LogicalPlan): Transformation[LogicalPlan] =
    normalize(plan).flatMap(_.transformUp { case TopPercent(child, percentage, withTies) =>
      if (withTies) {
        withPercentiles(child, percentage)
      } else {
        viaTotalCount(child, percentage)
      }
    })

  /** See [[PullLimitUpwards]] */
  private def normalize(plan: LogicalPlan): Transformation[LogicalPlan] = plan transformUp {
    case Project(TopPercent(child, limit, withTies), exprs) =>
      ok(TopPercent(Project(child, exprs), limit, withTies))
    case Filter(TopPercent(child, limit, withTies), cond) =>
      ok(TopPercent(Filter(child, cond), limit, withTies))
    case Sort(TopPercent(child, limit, withTies), order, global) =>
      ok(TopPercent(Sort(child, order, global), limit, withTies))
    case Offset(TopPercent(child, limit, withTies), offset) =>
      ok(TopPercent(Offset(child, offset), limit, withTies))
  }

  private def withPercentiles(child: LogicalPlan, percentage: Expression): Transformation[LogicalPlan] = {

    updatePhase { case o: Optimizing =>
      o.copy(freshNameCounter = o.freshNameCounter + 1)
    }.flatMap { _ =>
      getCurrentPhase.flatMap {
        case o: Optimizing =>
          val cteSuffix = o.freshNameCounter
          val originalCteName = s"_limited$cteSuffix"
          val withPercentileCteName = s"_with_percentile$cteSuffix"
          val percentileColName = s"_percentile$cteSuffix"

          child match {
            case Sort(child, order, _) =>
              // TODO: this is (temporary) hack due to the lack of star resolution. otherwise child.output is fine
              child
                .collectFirst { case Project(_, reProject) =>
                  ok(WithCTE(
                    Seq(
                      SubqueryAlias(child, Id(originalCteName)),
                      SubqueryAlias(
                        Project(
                          UnresolvedRelation(originalCteName, message = s"Unresolved $originalCteName"),
                          reProject ++ Seq(
                            Alias(Window(NTile(Literal(100)), sort_order = order), Id(percentileColName)))),
                        Id(withPercentileCteName))),
                    Filter(
                      Project(
                        UnresolvedRelation(withPercentileCteName, message = s"Unresolved $withPercentileCteName"),
                        reProject),
                      LessThanOrEqual(
                        UnresolvedAttribute(
                          percentileColName,
                          ruleText = percentileColName,
                          message = s"Unresolved $percentileColName"),
                        Divide(percentage, Literal(100))))))
                }
                .getOrElse(lift(PartialResult(child, UnexpectedNode("Cannot find a projection"))))
            case _ =>
              // TODO: (jimidle) figure out cases when this is not true
              lift(PartialResult(child, UnexpectedNode("TopPercent with ties requires a Sort node")))
          }

        case p => ko(WorkflowStage.OPTIMIZE, IncoherentState(p, classOf[Optimizing]))
      }
    }

  }

  private def viaTotalCount(child: LogicalPlan, percentage: Expression): Transformation[WithCTE] = {

    updatePhase { case o: Optimizing =>
      o.copy(freshNameCounter = o.freshNameCounter + 1)
    }.flatMap { _ =>
      getCurrentPhase.flatMap {
        case o: Optimizing =>
          val cteSuffix = o.freshNameCounter
          val originalCteName = s"_limited$cteSuffix"
          val countedCteName = s"_counted$cteSuffix"
          ok(
            WithCTE(
              Seq(
                SubqueryAlias(child, Id(originalCteName)),
                SubqueryAlias(
                  Project(
                    UnresolvedRelation(ruleText = originalCteName, message = s"Unresolved relation $originalCteName"),
                    Seq(Alias(Count(Seq(Star())), Id("count")))),
                  Id(countedCteName))),
              Limit(
                Project(
                  UnresolvedRelation(ruleText = originalCteName, message = s"Unresolved relation $originalCteName"),
                  Seq(Star())),
                ScalarSubquery(Project(
                  UnresolvedRelation(
                    ruleText = countedCteName,
                    message = s"Unresolved relation $countedCteName",
                    ruleName = "N/A",
                    tokenName = Some("N/A")),
                  Seq(Cast(Multiply(Divide(Id("count"), percentage), Literal(100)), LongType)))))))
        case phase => ko(WorkflowStage.OPTIMIZE, IncoherentState(phase, classOf[Optimizing]))
      }
    }

  }
}
