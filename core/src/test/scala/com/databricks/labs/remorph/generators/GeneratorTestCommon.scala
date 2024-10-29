package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.{OkResult, Optimized, intermediate => ir}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers

trait GeneratorTestCommon[T <: ir.TreeNode[T]] extends Matchers {

  protected def generator: Generator[T, String]

  implicit class TestOps(t: T) {
    def generates(expectedOutput: String): Assertion = {
      val exprGenerator = new ExpressionGenerator()
      val optionGenerator = new OptionGenerator(exprGenerator)
      val logical = new LogicalPlanGenerator(exprGenerator, optionGenerator)
      generator.generate(GeneratorContext(logical), t).runAndDiscardState(Optimized(t)) shouldBe OkResult(
        expectedOutput)
    }

    def doesNotTranspile: Assertion = {
      val exprGenerator = new ExpressionGenerator()
      val optionGenerator = new OptionGenerator(exprGenerator)
      val logical = new LogicalPlanGenerator(exprGenerator, optionGenerator)
      generator
        .generate(GeneratorContext(logical), t)
        .runAndDiscardState(Optimized(t))
        .isInstanceOf[OkResult[_]] shouldBe false
    }
  }
}
