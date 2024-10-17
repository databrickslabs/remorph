package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.Result
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers

trait TranspilerTestCommon extends Matchers with Formatter {

  protected def transpiler: Transpiler

  implicit class TranspilerTestOps(input: String) {
    def transpilesTo(expectedOutput: String): Assertion = {
      transpiler.transpile(SourceCode(input)) match {
        case Result.Success(output) => format(output) shouldBe format(expectedOutput)
        case Result.Failure(_, err) => fail(err.msg)
      }
    }
    def failsTranspilation: Assertion = {
      transpiler.transpile(SourceCode(input)) match {
        case Result.Failure(_, _) => succeed
        case _ => fail("query was expected to fail transpilation but didn't")
      }
    }
  }
}
