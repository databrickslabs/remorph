package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.{Result, intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.Assertion

trait GeneratorTestCommon[T <: ir.TreeNode[T]] extends Matchers {

  protected def generator: Generator[T, String]

  implicit class TestOps(t: T) {
    def generates(expectedOutput: String): Assertion = {
      val exprGenerator = new ExpressionGenerator()
      val optionGenerator = new OptionGenerator(exprGenerator)
      val logical = new LogicalPlanGenerator(exprGenerator, optionGenerator)
      generator.generate(GeneratorContext(logical), t) shouldBe Result.Success(expectedOutput)
    }

    def doesNotTranspile: Assertion = {
      val exprGenerator = new ExpressionGenerator()
      val optionGenerator = new OptionGenerator(exprGenerator)
      val logical = new LogicalPlanGenerator(exprGenerator, optionGenerator)
      generator.generate(GeneratorContext(logical), t).isSuccess shouldBe false
    }
  }
}
