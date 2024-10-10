package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.{intermediate => ir}
import org.scalactic.source.Position
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class FlattenNestedConcatSpec extends AnyWordSpec with Matchers {

  val optimizer = new FlattenNestedConcat

  implicit class Ops(e: ir.Expression) {
    def becomes(expected: ir.Expression)(implicit pos: Position): Assertion = {
      optimizer.flattenConcat.applyOrElse(e, (x: ir.Expression) => x) shouldBe expected
    }
  }

  "FlattenNestedConcat" should {
    "CONCAT(a, b)" in {
      ir.Concat(Seq(ir.Id("a"), ir.Id("b"))) becomes ir.Concat(Seq(ir.Id("a"), ir.Id("b")))
    }

    "CONCAT(CONCAT(a, b), c)" in {
      ir.Concat(Seq(ir.Concat(Seq(ir.Id("a"), ir.Id("b"))), ir.Id("c"))) becomes ir.Concat(
        Seq(ir.Id("a"), ir.Id("b"), ir.Id("c")))
    }

    "CONCAT(a, CONCAT(b, c))" in {
      ir.Concat(Seq(ir.Id("a"), ir.Concat(Seq(ir.Id("b"), ir.Id("c"))))) becomes ir.Concat(
        Seq(ir.Id("a"), ir.Id("b"), ir.Id("c")))
    }

    "CONCAT(CONCAT(a, b), CONCAT(c, d))" in {
      ir.Concat(Seq(ir.Concat(Seq(ir.Id("a"), ir.Id("b"))), ir.Concat(Seq(ir.Id("c"), ir.Id("d"))))) becomes ir.Concat(
        Seq(ir.Id("a"), ir.Id("b"), ir.Id("c"), ir.Id("d")))
    }

    "CONCAT(CONCAT(a, b), CONCAT(c, CONCAT(d, e)))" in {
      ir.Concat(
        Seq(
          ir.Concat(Seq(ir.Id("a"), ir.Id("b"))),
          ir.Concat(Seq(ir.Id("c"), ir.Concat(Seq(ir.Id("d"), ir.Id("e"))))))) becomes ir.Concat(
        Seq(ir.Id("a"), ir.Id("b"), ir.Id("c"), ir.Id("d"), ir.Id("e")))
    }
  }
}
