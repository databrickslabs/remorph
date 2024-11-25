package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.generators.{GeneratorContext, GeneratorTestCommon}
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.intermediate.{Batch, Expression}
import com.databricks.labs.remorph.{Generating, intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

// Only add tests here that require the TSqlCallMapper, or in the future any other transformer/rule
// that is specific to T-SQL. Otherwise they belong in ExpressionGeneratorTest.

class TSqlExpressionGeneratorTest
    extends AnyWordSpec
    with GeneratorTestCommon[ir.Expression]
    with MockitoSugar
    with ir.IRHelpers {

  override protected val generator = new ExpressionGenerator()

  private val optionGenerator = new OptionGenerator(generator)

  private val logical = new LogicalPlanGenerator(generator, optionGenerator)

  override protected def initialState(t: Expression): Generating =
    Generating(optimizedPlan = Batch(Seq.empty), currentNode = t, ctx = GeneratorContext(logical))
}
