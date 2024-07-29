package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException
import org.scalatest.matchers.should.Matchers
import org.scalatest.Assertion

trait GeneratorTestCommon[T <: ir.TreeNode[T]] extends Matchers {

  protected def generator: Generator[T, String]

  implicit class TestOps(t: T) {
    def generates(expectedOutput: String): Assertion = {
      generator.generate(GeneratorContext(), t) shouldBe expectedOutput
    }

    def doesNotTranspile: Assertion = {
      assertThrows[TranspileException](generator.generate(GeneratorContext(), t))
    }
  }
}
