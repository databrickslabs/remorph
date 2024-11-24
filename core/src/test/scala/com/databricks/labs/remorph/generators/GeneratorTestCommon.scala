package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Generating, OkResult, intermediate => ir}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers

trait GeneratorTestCommon[T <: ir.TreeNode[T]] extends Matchers {

  protected def generator: Generator[T, String]
  protected def initialState(t: T): Generating

  implicit class TestOps(t: T) {
    def generates(expectedOutput: String): Assertion = {
      generator.generate(t).runAndDiscardState(initialState(t)) shouldBe OkResult(expectedOutput)
    }

    def doesNotTranspile: Assertion = {
      generator
        .generate(t)
        .runAndDiscardState(initialState(t))
        .isInstanceOf[OkResult[_]] shouldBe false
    }
  }
}
