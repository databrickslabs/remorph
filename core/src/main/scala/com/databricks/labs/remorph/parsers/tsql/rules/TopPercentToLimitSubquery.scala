package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.intermediate._

import java.util.concurrent.atomic.AtomicLong

case class TopPercent(child: LogicalPlan, percentage: Expression, with_ties: Boolean = false) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

class TopPercentToLimitSubquery extends Rule[LogicalPlan] {
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
    child match {
      case Sort(child, order, _) =>
        // TODO: this is (temporary) hack due to the lack of star resolution. otherwise child.output is fine
        val reProject = child.find(_.isInstanceOf[Project]).map(_.asInstanceOf[Project]) match {
          case Some(Project(_, expressions)) => expressions
          case None =>
            throw new IllegalArgumentException("Cannot find a projection")
        }
        WithCTE(
          Seq(
            SubqueryAlias(child, Id(originalCteName)),
            SubqueryAlias(
              Project(
                UnresolvedRelation(originalCteName, message = s"Unresolved $originalCteName"),
                reProject ++ Seq(Alias(Window(NTile(Literal(100)), sort_order = order), Id(percentileColName)))),
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
              Divide(percentage, Literal(100)))))
      case _ =>
        // TODO: (jimidle) figure out cases when this is not true
        throw new IllegalArgumentException("TopPercent with ties requires a Sort node")
    }
  }

  private def viaTotalCount(child: LogicalPlan, percentage: Expression) = {
    val cteSuffix = counter.incrementAndGet()
    val originalCteName = s"_limited$cteSuffix"
    val countedCteName = s"_counted$cteSuffix"
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
        ScalarSubquery(
          Project(
            UnresolvedRelation(
              ruleText = countedCteName,
              message = s"Unresolved relation $countedCteName",
              ruleName = "N/A",
              tokenName = Some("N/A")),
            Seq(Cast(Multiply(Divide(Id("count"), percentage), Literal(100)), LongType))))))
  }
}
