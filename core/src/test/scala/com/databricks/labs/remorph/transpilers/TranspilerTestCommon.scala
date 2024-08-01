package com.databricks.labs.remorph.transpilers

import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers

trait TranspilerTestCommon extends Matchers {

  protected def transpiler: Transpiler

  implicit class TranspilerTestOps(input: String) {
    def transpilesTo(expectedOutput: String): Assertion = {
      transpiler.transpile(input) shouldBe expectedOutput
    }
  }
}
