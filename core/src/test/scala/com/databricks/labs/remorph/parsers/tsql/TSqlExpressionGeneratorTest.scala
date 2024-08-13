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

  "CHECKSUM_AGG" should {
    "transpile to MD5 function" in {
      ir.CallFunction("CHECKSUM_AGG", Seq(ir.Id("col1"))) generates "MD5(CONCAT_WS(',', ARRAY_AGG(col1)))"
    }
  }

  "SET_BIT" should {
    "transpile to bitwise logic" in {
      ir.CallFunction("SET_BIT", Seq(ir.Literal(42.toShort), ir.Literal(7.toShort), ir.Literal(0.toShort))) generates
        "42 & -1 ^ SHIFTLEFT(1, 7) | SHIFTRIGHT(0, 7)"

      ir.CallFunction("SET_BIT", Seq(ir.Literal(42.toShort), ir.Literal(7.toShort))) generates
        "42 | SHIFTLEFT(1, 7)"
    }
  }

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
