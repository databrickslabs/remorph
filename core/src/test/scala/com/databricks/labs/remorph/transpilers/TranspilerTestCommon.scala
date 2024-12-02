package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.coverage.ErrorEncoders
import com.databricks.labs.remorph.{Init, KoResult, OkResult, Parsing, PartialResult}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import io.circe.syntax._

trait TranspilerTestCommon extends Matchers with Formatter with ErrorEncoders {

  protected def transpiler: Transpiler

  implicit class TranspilerTestOps(input: String) {

    def transpilesTo(expectedOutput: String, failOnError: Boolean = true): Assertion = {
      val formattedExpectedOutput = format(expectedOutput)
      transpiler.transpile(Parsing(input)).runAndDiscardState(Init) match {
        case OkResult(output) =>
          val formattedOutput = format(output)
          formattedOutput shouldBe formattedExpectedOutput
        case PartialResult(output, err) =>
          if (failOnError) {
            fail(err.asJson.noSpaces)
          } else {
            val formattedOutput = format(output)
            formattedOutput shouldBe formattedExpectedOutput
          }
        case KoResult(_, err) => fail(err.asJson.noSpaces)
      }
    }
    def failsTranspilation: Assertion = {
      transpiler.transpile(Parsing(input)).runAndDiscardState(Init) match {
        case KoResult(_, _) => succeed
        case PartialResult(_, _) => succeed
        case x =>
          fail(s"query was expected to fail transpilation but didn't: $x")
      }
    }
  }
}
