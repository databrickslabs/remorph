package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.parsers.intermediate._

import java.util.concurrent.atomic.AtomicLong

case class TopPercent(child: LogicalPlan, percentage: Expression, with_ties: Boolean = false) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

object TopPercentToLimitSubquery extends Rule[LogicalPlan] {
  private val counter = new AtomicLong()
  override def apply(plan: LogicalPlan): LogicalPlan = normalize(plan) transformUp {
    case TopPercent(child, percentage, withTies) =>
      if (withTies) {
        withPercentiles(child, percentage)
      } else {
        viaTotalCount(child, percentage)
      }
  }

  /** See [[PullLimitUpwards]] */
  private def normalize(plan: LogicalPlan): LogicalPlan = plan transformUp {
    case Project(TopPercent(child, limit, withTies), exprs) =>
      TopPercent(Project(child, exprs), limit, withTies)
    case Filter(TopPercent(child, limit, withTies), cond) =>
      TopPercent(Filter(child, cond), limit, withTies)
    case Sort(TopPercent(child, limit, withTies), order, global) =>
      TopPercent(Sort(child, order, global), limit, withTies)
    case Offset(TopPercent(child, limit, withTies), offset) =>
      TopPercent(Offset(child, offset), limit, withTies)
  }

  private def withPercentiles(child: LogicalPlan, percentage: Expression) = {
    val cteSuffix = counter.incrementAndGet()
    val originalCteName = s"_limited$cteSuffix"
    val withPercentileCteName = s"_with_percentile$cteSuffix"
    val percentileColName = s"_percentile$cteSuffix"
    // TODO: inject Filter in the right place, as this code takes a shortcut
    //  and omits the existing ORDER BY, LIMIT, and OFFSET nodes.
    WithCTE(
      Seq(
        SubqueryAlias(child, Id(originalCteName)),
        SubqueryAlias(
          Project(
            UnresolvedRelation(originalCteName),
            child.output ++ Seq(
              Alias(
                Window(
                  NTile(Literal(100)),
                  sort_order = Seq(
                    // TODO: get a unit test
                  )),
                Seq(Id(percentileColName))))),
          Id(withPercentileCteName))),
      Filter(
        Project(UnresolvedRelation(withPercentileCteName), child.output),
        LessThanOrEqual(UnresolvedAttribute(percentileColName), Divide(percentage, Literal(100)))))
  }

  private def viaTotalCount(child: LogicalPlan, percentage: Expression) = {
    val cteSuffix = counter.incrementAndGet()
    val originalCteName = s"_limited$cteSuffix"
    WithCTE(
      Seq(
        SubqueryAlias(child, Id(originalCteName)),
        SubqueryAlias(
          Project(UnresolvedRelation(originalCteName), Seq(Alias(Count(Seq(Star())), Seq(Id("count"))))),
          Id(s"_counted$cteSuffix"))),
      Limit(
        Project(UnresolvedRelation(originalCteName), Seq(Star())),
        ScalarSubquery(
          Project(
            UnresolvedRelation(originalCteName),
            Seq(Cast(Multiply(Divide(Id("count"), percentage), Literal(100)), LongType))))))
  }
}
