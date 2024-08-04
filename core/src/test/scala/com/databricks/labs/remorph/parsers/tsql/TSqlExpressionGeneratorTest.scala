package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, GeneratorTestCommon}
import com.databricks.labs.remorph.parsers.intermediate.IRHelpers
import com.databricks.labs.remorph.parsers.tsql.rules.TSqlCallMapper
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

  override protected val generator = new ExpressionGenerator(new TSqlCallMapper)

  "DATEADD" should {
    "transpile to DATE_ADD" in {
      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("day"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) generates "DATE_ADD(col1, 42)"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("week"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "DATE_ADD(col1, 42 * 7)"
    }

    "transpile to ADD_MONTHS" in {
      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("Month"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "ADD_MONTHS(col1, 42)"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("qq"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "ADD_MONTHS(col1, 42 * 3)"
    }

    "transpile to INTERVAL" in {
      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("hour"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "col1 + INTERVAL 42 HOUR"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("minute"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "col1 + INTERVAL 42 MINUTE"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("second"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "col1 + INTERVAL 42 SECOND"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("millisecond"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "col1 + INTERVAL 42 MILLISECOND"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("mcs"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "col1 + INTERVAL 42 MICROSECOND"

      ir.CallFunction(
        "DATEADD",
        Seq(
          simplyNamedColumn("ns"),
          ir.Literal(42.toShort),
          simplyNamedColumn("col1"))) generates "col1 + INTERVAL 42 NANOSECOND"
    }
  }

}
