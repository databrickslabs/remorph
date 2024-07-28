package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.parsers.PlanComparison
import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TopPercentToLimitSubqueryTest extends AnyWordSpec with PlanComparison with Matchers with IRHelpers {
  "PERCENT applies" in {
    val out = TopPercentToLimitSubquery.apply(
      TopPercent(
        Project(
          namedTable("Employees"),
          Seq(Star())
        ),
        Literal(short = Some(10)),
      )
    )
    comparePlans(
      out,
      WithCTE(Seq(
        SubqueryAlias(
          Project(
            namedTable("Employees"),
            Seq(
              Star()
            )
          ),
          Id("_limited1")
        ),
        SubqueryAlias(
          Project(
            UnresolvedRelation("_limited1"),
            Seq(
              Alias(
                Count(
                  Seq(
                    Star()
                  )
                ),
                Seq(
                  Id("count")
                )
              )
            )
          ),
          Id("_counted1")
        )
      ), Limit(
        Project(
          UnresolvedRelation("_limited1"),
          Seq(Star())
        ),
        ScalarSubquery(
          Project(
            UnresolvedRelation("_counted1"),
            Seq(
              Cast(
                Multiply(
                  Divide(
                    Id("count"),
                    Literal(10)
                  ),
                  Literal(100)
                ),
                LongType
              )
            )
          )
        )
      ))
    )
  }
}
