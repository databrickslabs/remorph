package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph._
import com.databricks.labs.remorph.coverage.ErrorEncoders
import io.circe.syntax._
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers

trait TranspilerTestCommon extends Matchers with Formatter with ErrorEncoders {

  protected def transpiler: Transpiler

  implicit class TranspilerTestOps(input: String) {
    def transpilesTo(expectedOutput: String, failOnError: Boolean = true): Assertion = {
      val formattedExpectedOutput = format(expectedOutput)
      transpiler.transpile(PreProcessing(input)).runAndDiscardState(TranspilerState()) match {
        case OkResult(output) =>
          format(output)
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
      transpiler.transpile(PreProcessing(input)).runAndDiscardState(TranspilerState()) match {
        case KoResult(_, _) => succeed
        case PartialResult(_, _) => succeed
        case x =>
          fail(s"query was expected to fail transpilation but didn't: $x")
      }
    }
  }
}
