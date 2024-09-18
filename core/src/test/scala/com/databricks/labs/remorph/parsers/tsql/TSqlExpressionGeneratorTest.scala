package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, GeneratorTestCommon}
import com.databricks.labs.remorph.parsers.intermediate.IRHelpers
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

// Only add tests here that require the TSqlCallMapper, or in the future any other transformer/rule
// that is specific to T-SQL. Otherwise they belong in ExpressionGeneratorTest.

class TSqlExpressionGeneratorTest
    extends AnyWordSpec
    with GeneratorTestCommon[ir.Expression]
    with MockitoSugar
    with IRHelpers {

  override protected val generator = new ExpressionGenerator

}
