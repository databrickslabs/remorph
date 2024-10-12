package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.{intermediate => ir}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlCallMapperSpec extends AnyWordSpec with Matchers with ir.IRHelpers {

  private val tsqlCallMapper = new TSqlCallMapper

  implicit class CallMapperOps(fn: ir.Fn) {
    def becomes(expected: ir.Expression): Assertion = {
      tsqlCallMapper.convert(fn) shouldBe expected
    }
  }

  "CHECKSUM_AGG" should {
    "transpile to MD5 function" in {
      ir.CallFunction("CHECKSUM_AGG", Seq(ir.Id("col1"))) becomes ir.Md5(
        ir.ConcatWs(Seq(ir.StringLiteral(","), ir.CollectList(ir.Id("col1")))))
    }
  }

  "SET_BIT" should {
    "transpile to bitwise logic" in {
      ir.CallFunction("SET_BIT", Seq(ir.Literal(42.toShort), ir.Literal(7.toShort), ir.Literal(0.toShort))) becomes
        ir.BitwiseOr(
          ir.BitwiseAnd(
            ir.Literal(42.toShort),
            ir.BitwiseXor(ir.Literal(-1), ir.ShiftLeft(ir.Literal(1), ir.Literal(7.toShort)))),
          ir.ShiftRight(ir.Literal(0.toShort), ir.Literal(7.toShort)))

      ir.CallFunction("SET_BIT", Seq(ir.Literal(42.toShort), ir.Literal(7.toShort))) becomes
        ir.BitwiseOr(ir.Literal(42.toShort), ir.ShiftLeft(ir.Literal(1), ir.Literal(7.toShort)))
    }
  }

  "DATEADD" should {
    "transpile to DATE_ADD" in {
      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("day"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.DateAdd(
        simplyNamedColumn("col1"),
        ir.Literal(42.toShort))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("week"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.DateAdd(
        simplyNamedColumn("col1"),
        ir.Multiply(ir.Literal(42.toShort), ir.Literal(7)))
    }

    "transpile to ADD_MONTHS" in {
      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("Month"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.AddMonths(
        simplyNamedColumn("col1"),
        ir.Literal(42.toShort))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("qq"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.AddMonths(
        simplyNamedColumn("col1"),
        ir.Multiply(ir.Literal(42.toShort), ir.Literal(3)))
    }

    "transpile to INTERVAL" in {
      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("hour"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.Add(
        simplyNamedColumn("col1"),
        ir.KnownInterval(ir.Literal(42.toShort), ir.HOUR_INTERVAL))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("minute"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.Add(
        simplyNamedColumn("col1"),
        ir.KnownInterval(ir.Literal(42.toShort), ir.MINUTE_INTERVAL))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("second"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.Add(
        simplyNamedColumn("col1"),
        ir.KnownInterval(ir.Literal(42.toShort), ir.SECOND_INTERVAL))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("millisecond"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.Add(
        simplyNamedColumn("col1"),
        ir.KnownInterval(ir.Literal(42.toShort), ir.MILLISECOND_INTERVAL))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("mcs"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.Add(
        simplyNamedColumn("col1"),
        ir.KnownInterval(ir.Literal(42.toShort), ir.MICROSECOND_INTERVAL))

      ir.CallFunction(
        "DATEADD",
        Seq(simplyNamedColumn("ns"), ir.Literal(42.toShort), simplyNamedColumn("col1"))) becomes ir.Add(
        simplyNamedColumn("col1"),
        ir.KnownInterval(ir.Literal(42.toShort), ir.NANOSECOND_INTERVAL))
    }
  }

}
