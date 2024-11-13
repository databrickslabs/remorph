package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.parsers.PlanComparison
import com.databricks.labs.remorph.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class PullLimitUpwardsTest extends AnyWordSpec with PlanComparison with Matchers with IRHelpers {
  "from project" in {
    val out = PullLimitUpwards.apply(Project(Limit(namedTable("a"), Literal(10)), Seq(Star(None))))
    comparePlans(out, Limit(Project(namedTable("a"), Seq(Star())), Literal(10)))
  }

  "from project with filter" in {
    val out = PullLimitUpwards.apply(
      Filter(
        Project(Limit(namedTable("a"), Literal(10)), Seq(Star(None))),
        GreaterThan(UnresolvedAttribute("b"), Literal(1))))
    comparePlans(
      out,
      Limit(
        Filter(Project(namedTable("a"), Seq(Star())), GreaterThan(UnresolvedAttribute("b"), Literal(1))),
        Literal(10)))
  }

  "from project with filter order by" in {
    val out = PullLimitUpwards.apply(
      Sort(
        Filter(
          Project(Limit(namedTable("a"), Literal(10)), Seq(Star(None))),
          GreaterThan(UnresolvedAttribute("b"), Literal(1))),
        Seq(SortOrder(UnresolvedAttribute("b"))),
        is_global = false))
    comparePlans(
      out,
      Limit(
        Sort(
          Filter(Project(namedTable("a"), Seq(Star())), GreaterThan(UnresolvedAttribute("b"), Literal(1))),
          Seq(SortOrder(UnresolvedAttribute("b"))),
          is_global = false),
        Literal(10)))
  }

}
