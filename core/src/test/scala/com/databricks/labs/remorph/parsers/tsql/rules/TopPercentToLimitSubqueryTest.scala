package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.parsers.PlanComparison
import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TopPercentToLimitSubqueryTest extends AnyWordSpec with PlanComparison with Matchers with IRHelpers {
  "PERCENT applies" in {
    val out =
      (new TopPercentToLimitSubquery).apply(TopPercent(Project(namedTable("Employees"), Seq(Star())), Literal(10)))
    comparePlans(
      out,
      WithCTE(
        Seq(
          SubqueryAlias(Project(namedTable("Employees"), Seq(Star())), Id("_limited1")),
          SubqueryAlias(
            Project(UnresolvedRelation("_limited1"), Seq(Alias(Count(Seq(Star())), Id("count")))),
            Id("_counted1"))),
        Limit(
          Project(UnresolvedRelation("_limited1"), Seq(Star())),
          ScalarSubquery(
            Project(
              UnresolvedRelation("_counted1"),
              Seq(Cast(Multiply(Divide(Id("count"), Literal(10)), Literal(100)), LongType)))))))
  }

  "PERCENT WITH TIES applies" in {
    val out = (new TopPercentToLimitSubquery).apply(
      Sort(
        Project(TopPercent(namedTable("Employees"), Literal(10), with_ties = true), Seq(Star())),
        Seq(SortOrder(UnresolvedAttribute("a"))),
        is_global = false))
    comparePlans(
      out,
      WithCTE(
        Seq(
          SubqueryAlias(Project(namedTable("Employees"), Seq(Star())), Id("_limited1")),
          SubqueryAlias(
            Project(
              UnresolvedRelation("_limited1"),
              Seq(
                Star(),
                Alias(
                  Window(NTile(Literal(100)), sort_order = Seq(SortOrder(UnresolvedAttribute("a")))),
                  Id("_percentile1")))),
            Id("_with_percentile1"))),
        Filter(
          Project(UnresolvedRelation("_with_percentile1"), Seq(Star())),
          LessThanOrEqual(UnresolvedAttribute("_percentile1"), Divide(Literal(10), Literal(100))))))
  }
}
