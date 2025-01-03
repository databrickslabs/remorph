package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.{OkResult, TranspilerState, intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class DealiasLCAsSpec extends AnyWordSpec with Matchers {

  val dealiaser = new DealiasLCAs

  "DealiasLCAs" should {

    "dealias a LCA" in {
      val plan =
        ir.Project(
          ir.Filter(ir.NoTable, ir.GreaterThan(ir.Id("abs"), ir.Literal(42))),
          Seq(ir.Alias(ir.Abs(ir.Literal(-42)), ir.Id("abs"))))

      val result = dealiaser.transformPlan(plan).runAndDiscardState(TranspilerState())

      result shouldBe
        OkResult(
          ir.Project(
            ir.Filter(ir.NoTable, ir.GreaterThan(ir.Abs(ir.Literal(-42)), ir.Literal(42))),
            Seq(ir.Alias(ir.Abs(ir.Literal(-42)), ir.Id("abs")))))

    }

  }
}
