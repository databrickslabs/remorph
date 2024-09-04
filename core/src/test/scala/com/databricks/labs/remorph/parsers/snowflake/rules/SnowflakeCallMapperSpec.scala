package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeCallMapperSpec extends AnyWordSpec with Matchers {

  private val snowflakeCallMapper = new SnowflakeCallMapper

  implicit class CallMapperOps(fn: ir.Fn) {
    def becomes(expected: ir.Expression): Assertion = {
      snowflakeCallMapper.convert(fn) shouldBe expected
    }
  }

  "SnowflakeCallMapper" should {
    "translate Snowflake functions" in {

      ir.CallFunction("ARRAY_CAT", Seq(ir.Noop)) becomes ir.Concat(Seq(ir.Noop))

      ir.CallFunction("ARRAY_CONSTRUCT", Seq(ir.Noop)) becomes ir.CreateArray(Seq(ir.Noop))

      ir.CallFunction("BOOLAND_AGG", Seq(ir.Noop)) becomes ir.BoolAnd(ir.Noop)

      ir.CallFunction("DATEADD", Seq(ir.Literal(1), ir.Literal(2))) becomes ir.DateAdd(ir.Literal(1), ir.Literal(2))

      ir.CallFunction("EDITDISTANCE", Seq(ir.Literal(1), ir.Literal(2))) becomes ir.Levenshtein(
        ir.Literal(1),
        ir.Literal(2),
        None)

      ir.CallFunction("IFNULL", Seq(ir.Noop)) becomes ir.Coalesce(Seq(ir.Noop))

      ir.CallFunction("JSON_EXTRACT_PATH_TEXT", Seq(ir.Noop, ir.Literal("foo"))) becomes ir.GetJsonObject(
        ir.Noop,
        ir.Literal("$.foo"))

      ir.CallFunction("JSON_EXTRACT_PATH_TEXT", Seq(ir.Noop, ir.Id("foo"))) becomes ir.GetJsonObject(
        ir.Noop,
        ir.Concat(Seq(ir.Literal("$."), ir.Id("foo"))))

      ir.CallFunction("LEN", Seq(ir.Noop)) becomes ir.Length(ir.Noop)

      ir.CallFunction("LISTAGG", Seq(ir.Literal(1), ir.Literal(2))) becomes ir.ArrayJoin(
        ir.CollectList(ir.Literal(1), None),
        ir.Literal(2),
        None)

      ir.CallFunction("MONTHNAME", Seq(ir.Noop)) becomes ir.DateFormatClass(ir.Noop, ir.Literal("MMM"))

      ir.CallFunction("OBJECT_KEYS", Seq(ir.Noop)) becomes ir.JsonObjectKeys(ir.Noop)

      ir.CallFunction("POSITION", Seq(ir.Noop)) becomes ir.CallFunction("LOCATE", Seq(ir.Noop))

      ir.CallFunction("REGEXP_LIKE", Seq(ir.Literal(1), ir.Literal(2))) becomes ir.RLike(ir.Literal(1), ir.Literal(2))

      ir.CallFunction("SPLIT_PART", Seq(ir.Literal("foo,bar"), ir.Literal(","), ir.Literal(0))) becomes ir
        .StringSplitPart(ir.Literal("foo,bar"), ir.Literal(","), ir.Literal(1))

      ir.CallFunction("SPLIT_PART", Seq(ir.Literal("foo,bar"), ir.Literal(","), ir.Literal(1))) becomes ir
        .StringSplitPart(ir.Literal("foo,bar"), ir.Literal(","), ir.Literal(1))

      ir.CallFunction("SPLIT_PART", Seq(ir.Literal("foo,bar"), ir.Literal(","), ir.Literal(4))) becomes ir
        .StringSplitPart(ir.Literal("foo,bar"), ir.Literal(","), ir.Literal(4))

      ir.CallFunction("SPLIT_PART", Seq(ir.Literal("foo,bar"), ir.Literal(","), ir.Id("c1"))) becomes ir
        .StringSplitPart(
          ir.Literal("foo,bar"),
          ir.Literal(","),
          ir.If(ir.Equals(ir.Id("c1"), ir.Literal(0)), ir.Literal(1), ir.Id("c1")))

      ir.CallFunction("SQUARE", Seq(ir.Noop)) becomes ir.Pow(ir.Noop, ir.Literal(2))

      ir.CallFunction("STRTOK_TO_ARRAY", Seq(ir.Literal("abc,def"), ir.Literal(","))) becomes ir.StringSplit(
        ir.Literal("abc,def"),
        ir.Literal("[,]"),
        None)

      ir.CallFunction("STRTOK_TO_ARRAY", Seq(ir.Literal("abc,def"), ir.Id("c1"))) becomes ir.StringSplit(
        ir.Literal("abc,def"),
        ir.Concat(Seq(ir.Literal("["), ir.Id("c1"), ir.Literal("]"))),
        None)

      ir.CallFunction("TO_DOUBLE", Seq(ir.Noop)) becomes ir.CallFunction("DOUBLE", Seq(ir.Noop))

      ir.CallFunction("TO_NUMBER", Seq(ir.Literal("$123.5"), ir.Literal("$999.0"))) becomes ir.ToNumber(
        ir.Literal("$123.5"),
        ir.Literal("$999.0"))

      ir.CallFunction("TO_NUMBER", Seq(ir.Literal("$123.5"), ir.Literal("$999.0"), ir.Literal(26))) becomes ir.Cast(
        ir.ToNumber(ir.Literal("$123.5"), ir.Literal("$999.0")),
        ir.DecimalType(Some(26), None))

      ir.CallFunction(
        "TO_NUMBER",
        Seq(ir.Literal("$123.5"), ir.Literal("$999.0"), ir.Literal(26), ir.Literal(4))) becomes ir.Cast(
        ir.ToNumber(ir.Literal("$123.5"), ir.Literal("$999.0")),
        ir.DecimalType(Some(26), Some(4)))

      ir.CallFunction("TO_NUMBER", Seq(ir.Literal("$123.5"), ir.Literal(26), ir.Literal(4))) becomes ir.Cast(
        ir.Literal("$123.5"),
        ir.DecimalType(Some(26), Some(4)))

      ir.CallFunction("TO_OBJECT", Seq(ir.Literal(1), ir.Literal(2))) becomes ir.StructsToJson(
        ir.Literal(1),
        Some(ir.Literal(2)))

      ir.CallFunction("TRY_TO_NUMBER", Seq(ir.Literal("$123.5"), ir.Literal("$999.0"), ir.Literal(26))) becomes ir.Cast(
        ir.TryToNumber(ir.Literal("$123.5"), ir.Literal("$999.0")),
        ir.DecimalType(Some(26), Some(0)))

      ir.CallFunction(
        "TRY_TO_NUMBER",
        Seq(ir.Literal("$123.5"), ir.Literal("$999.0"), ir.Literal(26), ir.Literal(4))) becomes ir.Cast(
        ir.TryToNumber(ir.Literal("$123.5"), ir.Literal("$999.0")),
        ir.DecimalType(Some(26), Some(4)))

      ir.CallFunction("TRY_TO_NUMBER", Seq(ir.Literal("$123.5"), ir.Literal(26), ir.Literal(4))) becomes ir.Cast(
        ir.Literal("$123.5"),
        ir.DecimalType(Some(26), Some(4)))

    }

    "ARRAY_SLICE index shift" in {
      ir.CallFunction("ARRAY_SLICE", Seq(ir.Id("arr1"), ir.IntLiteral(0), ir.IntLiteral(2))) becomes ir.Slice(
        ir.Id("arr1"),
        ir.IntLiteral(1),
        ir.IntLiteral(2))

      ir.CallFunction("ARRAY_SLICE", Seq(ir.Id("arr1"), ir.UMinus(ir.IntLiteral(2)), ir.IntLiteral(2))) becomes ir
        .Slice(ir.Id("arr1"), ir.UMinus(ir.IntLiteral(2)), ir.IntLiteral(2))

      ir.CallFunction("ARRAY_SLICE", Seq(ir.Id("arr1"), ir.Id("col1"), ir.IntLiteral(2))) becomes ir
        .Slice(
          ir.Id("arr1"),
          ir.If(
            ir.GreaterThanOrEqual(ir.Id("col1"), ir.IntLiteral(0)),
            ir.Add(ir.Id("col1"), ir.IntLiteral(1)),
            ir.Id("col1")),
          ir.IntLiteral(2))
    }
  }
}
