package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import upickle.default._

trait TranspilerTestCommon extends Matchers with Formatter {

  protected def transpiler: Transpiler

  protected def reformat = true

  private def formatResult(result: String): String = if (reformat) format(result) else result

  implicit class TranspilerTestOps(input: String) {
    def transpilesTo(expectedOutput: String): Assertion = {
      transpiler.transpile(SourceCode(input)) match {
        case OkResult(output) => formatResult(output) shouldBe formatResult(expectedOutput)
        case PartialResult(_, err) => fail(write(err))
        case KoResult(_, err) => fail(write(err))
      }
    }
    def failsTranspilation: Assertion = {
      transpiler.transpile(SourceCode(input)) match {
        case KoResult(_, _) => succeed
        case PartialResult(_, _) => succeed
        case _ => fail("query was expected to fail transpilation but didn't")
      }
    }
  }
}
