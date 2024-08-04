package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class ExpressionGeneratorTest extends AnyWordSpec with GeneratorTestCommon[ir.Expression] with MockitoSugar {

  override protected val generator = new ExpressionGenerator

  "options" in {
    ir.Options(
      Map(
        "KEEPFIXED" -> ir.Column(None, ir.Id("PLAN")),
        "FAST" -> ir.Literal(short = Some(666)),
        "MAX_GRANT_PERCENT" -> ir.Literal(short = Some(30))),
      Map(),
      Map("FLAME" -> false, "QUICKLY" -> true),
      List()) generates
      """/*
      |   The following statement was originally given the following OPTIONS:
      |
      |    Expression options:
      |
      |     KEEPFIXED = PLAN
      |     FAST = 666
      |     MAX_GRANT_PERCENT = 30
      |
      |    Boolean options:
      |
      |     FLAME OFF
      |     QUICKLY ON
      |
      |
      | */
      |""".stripMargin
  }

  "columns" in {
    ir.UnresolvedAttribute("a") generates "a"
    ir.Column(None, ir.Id("a")) generates "a"
    ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("a")) generates "t.a"
    ir.Column(Some(ir.ObjectReference(ir.Id("s.t"))), ir.Id("a")) generates "s.t.a"
  }

  "arithmetic" in {
    ir.UMinus(ir.UnresolvedAttribute("a")) generates "-a"
    ir.UPlus(ir.UnresolvedAttribute("a")) generates "+a"
    ir.Multiply(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a * b"
    ir.Divide(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a / b"
    ir.Mod(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a % b"
    ir.Add(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a + b"
    ir.Subtract(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a - b"
  }

  "bitwise" in {
    ir.BitwiseOr(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a | b"
    ir.BitwiseAnd(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a & b"
    ir.BitwiseXor(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a ^ b"
    ir.BitwiseNot(ir.UnresolvedAttribute("a")) generates "~a"
  }

  "like" in {
    ir.Like(ir.UnresolvedAttribute("a"), ir.Literal("b%")) generates "a LIKE 'b%'"
    ir.Like(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"), '/') generates "a LIKE b ESCAPE '/'"
  }

  "predicates" should {
    "be generated" in {
      ir.And(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "(a AND b)"
      ir.Or(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "(a OR b)"
      ir.Not(ir.UnresolvedAttribute("a")) generates "NOT (a)"
      ir.Equals(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a = b"
      ir.NotEquals(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a != b"
      ir.LessThan(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a < b"
      ir.LessThanOrEqual(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a <= b"
      ir.GreaterThan(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a > b"
      ir.GreaterThanOrEqual(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a >= b"
    }
  }

  "functions" should {
    "be generated" in {
      ir.CallFunction("ABS", Seq(ir.UnresolvedAttribute("a"))) generates "ABS(a)"
      ir.CallFunction("ACOS", Seq(ir.UnresolvedAttribute("a"))) generates "ACOS(a)"
      ir.CallFunction("ACOSH", Seq(ir.UnresolvedAttribute("a"))) generates "ACOSH(a)"

      ir.CallFunction(
        "ADD_MONTHS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ADD_MONTHS(a, b)"

      ir.CallFunction(
        "AGGREGATE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "AGGREGATE(a, b, c, d)"
      ir.CallFunction("ANY", Seq(ir.UnresolvedAttribute("a"))) generates "ANY(a)"

      ir.CallFunction(
        "APPROX_COUNT_DISTINCT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "APPROX_COUNT_DISTINCT(a, b)"

      ir.CallFunction(
        "ARRAY",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "ARRAY(a, b, c, d)"

      ir.CallFunction(
        "ARRAYS_OVERLAP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAYS_OVERLAP(a, b)"

      ir.CallFunction(
        "ARRAYS_ZIP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAYS_ZIP(a, b)"

      ir.CallFunction(
        "ARRAY_CONTAINS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_CONTAINS(a, b)"
      ir.CallFunction("ARRAY_DISTINCT", Seq(ir.UnresolvedAttribute("a"))) generates "ARRAY_DISTINCT(a)"

      ir.CallFunction(
        "ARRAY_EXCEPT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_EXCEPT(a, b)"

      ir.CallFunction(
        "ARRAY_INTERSECT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_INTERSECT(a, b)"

      ir.CallFunction(
        "ARRAY_JOIN",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "ARRAY_JOIN(a, b, c)"
      ir.CallFunction("ARRAY_MAX", Seq(ir.UnresolvedAttribute("a"))) generates "ARRAY_MAX(a)"
      ir.CallFunction("ARRAY_MIN", Seq(ir.UnresolvedAttribute("a"))) generates "ARRAY_MIN(a)"

      ir.CallFunction(
        "ARRAY_POSITION",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_POSITION(a, b)"

      ir.CallFunction(
        "ARRAY_REMOVE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_REMOVE(a, b)"

      ir.CallFunction(
        "ARRAY_REPEAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_REPEAT(a, b)"

      ir.CallFunction(
        "ARRAY_SORT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_SORT(a, b)"

      ir.CallFunction(
        "ARRAY_UNION",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_UNION(a, b)"
      ir.CallFunction("ASCII", Seq(ir.UnresolvedAttribute("a"))) generates "ASCII(a)"
      ir.CallFunction("ASIN", Seq(ir.UnresolvedAttribute("a"))) generates "ASIN(a)"
      ir.CallFunction("ASINH", Seq(ir.UnresolvedAttribute("a"))) generates "ASINH(a)"

      ir.CallFunction(
        "ASSERT_TRUE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ASSERT_TRUE(a, b)"
      ir.CallFunction("ATAN", Seq(ir.UnresolvedAttribute("a"))) generates "ATAN(a)"

      ir.CallFunction("ATAN2", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ATAN2(a, b)"
      ir.CallFunction("ATANH", Seq(ir.UnresolvedAttribute("a"))) generates "ATANH(a)"
      ir.CallFunction("AVG", Seq(ir.UnresolvedAttribute("a"))) generates "AVG(a)"
      ir.CallFunction("BASE64", Seq(ir.UnresolvedAttribute("a"))) generates "BASE64(a)"
      ir.CallFunction("BIN", Seq(ir.UnresolvedAttribute("a"))) generates "BIN(a)"
      ir.CallFunction("BIT_AND", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_AND(a)"
      ir.CallFunction("BIT_COUNT", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_COUNT(a)"
      ir.CallFunction("BIT_LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_LENGTH(a)"
      ir.CallFunction("BIT_OR", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_OR(a)"
      ir.CallFunction("BIT_XOR", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_XOR(a)"
      ir.CallFunction("BOOL_AND", Seq(ir.UnresolvedAttribute("a"))) generates "BOOL_AND(a)"

      ir.CallFunction("BROUND", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "BROUND(a, b)"
      ir.CallFunction("CBRT", Seq(ir.UnresolvedAttribute("a"))) generates "CBRT(a)"
      ir.CallFunction("CEIL", Seq(ir.UnresolvedAttribute("a"))) generates "CEIL(a)"
      ir.CallFunction("CHAR", Seq(ir.UnresolvedAttribute("a"))) generates "CHAR(a)"

      ir.CallFunction(
        "COALESCE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COALESCE(a, b)"
      ir.CallFunction("COLLECT_LIST", Seq(ir.UnresolvedAttribute("a"))) generates "COLLECT_LIST(a)"
      ir.CallFunction("COLLECT_SET", Seq(ir.UnresolvedAttribute("a"))) generates "COLLECT_SET(a)"

      ir.CallFunction("CONCAT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CONCAT(a, b)"

      ir.CallFunction(
        "CONCAT_WS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CONCAT_WS(a, b)"

      ir.CallFunction(
        "CONV",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "CONV(a, b, c)"

      ir.CallFunction("CORR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CORR(a, b)"
      ir.CallFunction("COS", Seq(ir.UnresolvedAttribute("a"))) generates "COS(a)"
      ir.CallFunction("COSH", Seq(ir.UnresolvedAttribute("a"))) generates "COSH(a)"
      ir.CallFunction("COT", Seq(ir.UnresolvedAttribute("a"))) generates "COT(a)"

      ir.CallFunction("COUNT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COUNT(a, b)"
      ir.CallFunction("COUNT_IF", Seq(ir.UnresolvedAttribute("a"))) generates "COUNT_IF(a)"

      ir.CallFunction(
        "COUNT_MIN_SKETCH",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "COUNT_MIN_SKETCH(a, b, c, d)"

      ir.CallFunction(
        "COVAR_POP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COVAR_POP(a, b)"

      ir.CallFunction(
        "COVAR_SAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COVAR_SAMP(a, b)"
      ir.CallFunction("CRC32", Seq(ir.UnresolvedAttribute("a"))) generates "CRC32(a)"

      ir.CallFunction("CUBE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CUBE(a, b)"
      ir.CallFunction("CUME_DIST", Seq()) generates "CUME_DIST()"
      ir.CallFunction("CURRENT_CATALOG", Seq()) generates "CURRENT_CATALOG()"
      ir.CallFunction("CURRENT_DATABASE", Seq()) generates "CURRENT_DATABASE()"
      ir.CallFunction("CURRENT_DATE", Seq()) generates "CURRENT_DATE()"
      ir.CallFunction("CURRENT_TIMESTAMP", Seq()) generates "CURRENT_TIMESTAMP()"
      ir.CallFunction("CURRENT_TIMEZONE", Seq()) generates "CURRENT_TIMEZONE()"

      ir.CallFunction(
        "DATEDIFF",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATEDIFF(a, b)"

      ir.CallFunction(
        "DATE_ADD",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_ADD(a, b)"

      ir.CallFunction(
        "DATE_FORMAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_FORMAT(a, b)"

      ir.CallFunction("DATE_FROM_UNIX_DATE", Seq(ir.UnresolvedAttribute("a"))) generates "DATE_FROM_UNIX_DATE(a)"

      ir.CallFunction(
        "DATE_PART",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_PART(a, b)"

      ir.CallFunction(
        "DATE_SUB",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_SUB(a, b)"

      ir.CallFunction(
        "DATE_TRUNC",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_TRUNC(a, b)"
      ir.CallFunction("DAYOFMONTH", Seq(ir.UnresolvedAttribute("a"))) generates "DAYOFMONTH(a)"
      ir.CallFunction("DAYOFWEEK", Seq(ir.UnresolvedAttribute("a"))) generates "DAYOFWEEK(a)"
      ir.CallFunction("DAYOFYEAR", Seq(ir.UnresolvedAttribute("a"))) generates "DAYOFYEAR(a)"

      ir.CallFunction("DECODE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DECODE(a, b)"
      ir.CallFunction("DEGREES", Seq(ir.UnresolvedAttribute("a"))) generates "DEGREES(a)"

      ir.CallFunction(
        "DENSE_RANK",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DENSE_RANK(a, b)"

      ir.CallFunction("DIV", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DIV(a, b)"
      ir.CallFunction("E", Seq()) generates "E()"

      ir.CallFunction(
        "ELEMENT_AT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ELEMENT_AT(a, b)"

      ir.CallFunction("ELT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ELT(a, b)"

      ir.CallFunction("ENCODE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ENCODE(a, b)"

      ir.CallFunction("EXISTS", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "EXISTS(a, b)"
      ir.CallFunction("EXP", Seq(ir.UnresolvedAttribute("a"))) generates "EXP(a)"
      ir.CallFunction("EXPLODE", Seq(ir.UnresolvedAttribute("a"))) generates "EXPLODE(a)"
      ir.CallFunction("EXPM1", Seq(ir.UnresolvedAttribute("a"))) generates "EXPM1(a)"

      ir.CallFunction(
        "EXTRACT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "EXTRACT(a, b)"
      ir.CallFunction("FACTORIAL", Seq(ir.UnresolvedAttribute("a"))) generates "FACTORIAL(a)"

      ir.CallFunction("FILTER", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FILTER(a, b)"

      ir.CallFunction(
        "FIND_IN_SET",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FIND_IN_SET(a, b)"

      ir.CallFunction("FIRST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FIRST(a, b)"
      ir.CallFunction("FLATTEN", Seq(ir.UnresolvedAttribute("a"))) generates "FLATTEN(a)"
      ir.CallFunction("FLOOR", Seq(ir.UnresolvedAttribute("a"))) generates "FLOOR(a)"

      ir.CallFunction("FORALL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FORALL(a, b)"

      ir.CallFunction(
        "FORMAT_NUMBER",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FORMAT_NUMBER(a, b)"

      ir.CallFunction(
        "FORMAT_STRING",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FORMAT_STRING(a, b)"

      ir.CallFunction(
        "FROM_CSV",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "FROM_CSV(a, b, c)"

      ir.CallFunction(
        "FROM_JSON",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "FROM_JSON(a, b, c)"

      ir.CallFunction(
        "FROM_UNIXTIME",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FROM_UNIXTIME(a, b)"

      ir.CallFunction(
        "FROM_UTC_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FROM_UTC_TIMESTAMP(a, b)"

      ir.CallFunction(
        "GET_JSON_OBJECT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "GET_JSON_OBJECT(a, b)"

      ir.CallFunction(
        "GREATEST",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "GREATEST(a, b)"
      ir.CallFunction("GROUPING", Seq(ir.UnresolvedAttribute("a"))) generates "GROUPING(a)"

      ir.CallFunction(
        "GROUPING_ID",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "GROUPING_ID(a, b)"

      ir.CallFunction("HASH", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "HASH(a, b)"
      ir.CallFunction("HEX", Seq(ir.UnresolvedAttribute("a"))) generates "HEX(a)"
      ir.CallFunction("HOUR", Seq(ir.UnresolvedAttribute("a"))) generates "HOUR(a)"

      ir.CallFunction("HYPOT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "HYPOT(a, b)"

      ir.CallFunction(
        "IF",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "IF(a, b, c)"

      ir.CallFunction("IFNULL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "IFNULL(a, b)"
      ir.CallFunction("INITCAP", Seq(ir.UnresolvedAttribute("a"))) generates "INITCAP(a)"
      ir.CallFunction("INLINE", Seq(ir.UnresolvedAttribute("a"))) generates "INLINE(a)"
      ir.CallFunction("INPUT_FILE_BLOCK_LENGTH", Seq()) generates "INPUT_FILE_BLOCK_LENGTH()"
      ir.CallFunction("INPUT_FILE_BLOCK_START", Seq()) generates "INPUT_FILE_BLOCK_START()"
      ir.CallFunction("INPUT_FILE_NAME", Seq()) generates "INPUT_FILE_NAME()"

      ir.CallFunction("INSTR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "INSTR(a, b)"
      ir.CallFunction("ISNAN", Seq(ir.UnresolvedAttribute("a"))) generates "ISNAN(a)"
      ir.CallFunction("ISNOTNULL", Seq(ir.UnresolvedAttribute("a"))) generates "ISNOTNULL(a)"
      ir.CallFunction("ISNULL", Seq(ir.UnresolvedAttribute("a"))) generates "ISNULL(a)"

      ir.CallFunction(
        "JAVA_METHOD",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "JAVA_METHOD(a, b)"
      ir.CallFunction("JSON_ARRAY_LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "JSON_ARRAY_LENGTH(a)"
      ir.CallFunction("JSON_OBJECT_KEYS", Seq(ir.UnresolvedAttribute("a"))) generates "JSON_OBJECT_KEYS(a)"

      ir.CallFunction(
        "JSON_TUPLE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "JSON_TUPLE(a, b)"
      ir.CallFunction("KURTOSIS", Seq(ir.UnresolvedAttribute("a"))) generates "KURTOSIS(a)"

      ir.CallFunction(
        "LAG",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "LAG(a, b, c)"

      ir.CallFunction("LAST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LAST(a, b)"
      ir.CallFunction("LAST_DAY", Seq(ir.UnresolvedAttribute("a"))) generates "LAST_DAY(a)"

      ir.CallFunction(
        "LEAD",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "LEAD(a, b, c)"

      ir.CallFunction("LEAST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LEAST(a, b)"

      ir.CallFunction("LEFT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LEFT(a, b)"
      ir.CallFunction("LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "LENGTH(a)"

      ir.CallFunction(
        "LEVENSHTEIN",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LEVENSHTEIN(a, b)"
      ir.CallFunction("LN", Seq(ir.UnresolvedAttribute("a"))) generates "LN(a)"

      ir.CallFunction("LOG", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LOG(a, b)"
      ir.CallFunction("LOG10", Seq(ir.UnresolvedAttribute("a"))) generates "LOG10(a)"
      ir.CallFunction("LOG1P", Seq(ir.UnresolvedAttribute("a"))) generates "LOG1P(a)"
      ir.CallFunction("LOG2", Seq(ir.UnresolvedAttribute("a"))) generates "LOG2(a)"
      ir.CallFunction("LOWER", Seq(ir.UnresolvedAttribute("a"))) generates "LOWER(a)"

      ir.CallFunction("LTRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LTRIM(a, b)"

      ir.CallFunction(
        "MAKE_DATE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "MAKE_DATE(a, b, c)"

      ir.CallFunction(
        "MAP_CONCAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAP_CONCAT(a, b)"
      ir.CallFunction("MAP_ENTRIES", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_ENTRIES(a)"

      ir.CallFunction(
        "MAP_FILTER",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAP_FILTER(a, b)"

      ir.CallFunction(
        "MAP_FROM_ARRAYS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAP_FROM_ARRAYS(a, b)"
      ir.CallFunction("MAP_FROM_ENTRIES", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_FROM_ENTRIES(a)"
      ir.CallFunction("MAP_KEYS", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_KEYS(a)"
      ir.CallFunction("MAP_VALUES", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_VALUES(a)"

      ir.CallFunction(
        "MAP_ZIP_WITH",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "MAP_ZIP_WITH(a, b, c)"
      ir.CallFunction("MAX", Seq(ir.UnresolvedAttribute("a"))) generates "MAX(a)"

      ir.CallFunction("MAX_BY", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAX_BY(a, b)"
      ir.CallFunction("MD5", Seq(ir.UnresolvedAttribute("a"))) generates "MD5(a)"
      ir.CallFunction("MIN", Seq(ir.UnresolvedAttribute("a"))) generates "MIN(a)"
      ir.CallFunction("MINUTE", Seq(ir.UnresolvedAttribute("a"))) generates "MINUTE(a)"

      ir.CallFunction("MIN_BY", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MIN_BY(a, b)"

      ir.CallFunction("MOD", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MOD(a, b)"
      ir.CallFunction("MONOTONICALLY_INCREASING_ID", Seq()) generates "MONOTONICALLY_INCREASING_ID()"
      ir.CallFunction("MONTH", Seq(ir.UnresolvedAttribute("a"))) generates "MONTH(a)"

      ir.CallFunction(
        "MONTHS_BETWEEN",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "MONTHS_BETWEEN(a, b, c)"

      ir.CallFunction(
        "NAMED_STRUCT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NAMED_STRUCT(a, b)"

      ir.CallFunction("NANVL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NANVL(a, b)"
      ir.CallFunction("NEGATIVE", Seq(ir.UnresolvedAttribute("a"))) generates "NEGATIVE(a)"

      ir.CallFunction(
        "NEXT_DAY",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NEXT_DAY(a, b)"
      ir.CallFunction("NOW", Seq()) generates "NOW()"

      ir.CallFunction(
        "NTH_VALUE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NTH_VALUE(a, b)"
      ir.CallFunction("NTILE", Seq(ir.UnresolvedAttribute("a"))) generates "NTILE(a)"

      ir.CallFunction("NULLIF", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NULLIF(a, b)"

      ir.CallFunction("NVL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NVL(a, b)"

      ir.CallFunction(
        "NVL2",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "NVL2(a, b, c)"
      ir.CallFunction("OCTET_LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "OCTET_LENGTH(a)"
      ir.CallFunction("OR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "OR(a, b)"

      ir.CallFunction(
        "OVERLAY",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "OVERLAY(a, b, c, d)"

      ir.CallFunction(
        "PARSE_URL",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "PARSE_URL(a, b)"

      ir.CallFunction(
        "PERCENTILE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "PERCENTILE(a, b, c)"

      ir.CallFunction(
        "PERCENTILE_APPROX",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "PERCENTILE_APPROX(a, b, c)"

      ir.CallFunction(
        "PERCENT_RANK",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "PERCENT_RANK(a, b)"
      ir.CallFunction("PI", Seq()) generates "PI()"

      ir.CallFunction("PMOD", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "PMOD(a, b)"
      ir.CallFunction("POSEXPLODE", Seq(ir.UnresolvedAttribute("a"))) generates "POSEXPLODE(a)"
      ir.CallFunction("POSITIVE", Seq(ir.UnresolvedAttribute("a"))) generates "POSITIVE(a)"

      ir.CallFunction("POW", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "POW(a, b)"
      ir.CallFunction("QUARTER", Seq(ir.UnresolvedAttribute("a"))) generates "QUARTER(a)"
      ir.CallFunction("RADIANS", Seq(ir.UnresolvedAttribute("a"))) generates "RADIANS(a)"
      ir.CallFunction("RAISE_ERROR", Seq(ir.UnresolvedAttribute("a"))) generates "RAISE_ERROR(a)"
      ir.CallFunction("RAND", Seq(ir.UnresolvedAttribute("a"))) generates "RAND(a)"
      ir.CallFunction("RANDN", Seq(ir.UnresolvedAttribute("a"))) generates "RANDN(a)"

      ir.CallFunction("RANK", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "RANK(a, b)"

      ir.CallFunction(
        "REGEXP_EXTRACT",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "REGEXP_EXTRACT(a, b, c)"

      ir.CallFunction(
        "REGEXP_EXTRACT_ALL",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "REGEXP_EXTRACT_ALL(a, b, c)"

      ir.CallFunction(
        "REGEXP_REPLACE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "REGEXP_REPLACE(a, b, c, d)"

      ir.CallFunction("REPEAT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "REPEAT(a, b)"

      ir.CallFunction(
        "REPLACE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "REPLACE(a, b, c)"
      ir.CallFunction("REVERSE", Seq(ir.UnresolvedAttribute("a"))) generates "REVERSE(a)"

      ir.CallFunction("RIGHT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "RIGHT(a, b)"
      ir.CallFunction("RINT", Seq(ir.UnresolvedAttribute("a"))) generates "RINT(a)"

      ir.CallFunction("RLIKE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "a RLIKE b"

      ir.CallFunction("ROLLUP", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ROLLUP(a, b)"

      ir.CallFunction("ROUND", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ROUND(a, b)"
      ir.CallFunction("ROW_NUMBER", Seq()) generates "ROW_NUMBER()"

      ir.CallFunction(
        "RPAD",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "RPAD(a, b, c)"

      ir.CallFunction("RTRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "RTRIM(a, b)"

      ir.CallFunction(
        "SCHEMA_OF_CSV",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SCHEMA_OF_CSV(a, b)"

      ir.CallFunction(
        "SCHEMA_OF_JSON",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SCHEMA_OF_JSON(a, b)"
      ir.CallFunction("SECOND", Seq(ir.UnresolvedAttribute("a"))) generates "SECOND(a)"

      ir.CallFunction(
        "SENTENCES",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SENTENCES(a, b, c)"

      ir.CallFunction(
        "SEQUENCE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SEQUENCE(a, b, c)"
      ir.CallFunction("SHA", Seq(ir.UnresolvedAttribute("a"))) generates "SHA(a)"

      ir.CallFunction("SHA2", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHA2(a, b)"

      ir.CallFunction(
        "SHIFTLEFT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHIFTLEFT(a, b)"

      ir.CallFunction(
        "SHIFTRIGHT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHIFTRIGHT(a, b)"

      ir.CallFunction(
        "SHIFTRIGHTUNSIGNED",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHIFTRIGHTUNSIGNED(a, b)"
      ir.CallFunction("SHUFFLE", Seq(ir.UnresolvedAttribute("a"))) generates "SHUFFLE(a)"
      ir.CallFunction("SIGN", Seq(ir.UnresolvedAttribute("a"))) generates "SIGN(a)"
      ir.CallFunction("SIN", Seq(ir.UnresolvedAttribute("a"))) generates "SIN(a)"
      ir.CallFunction("SINH", Seq(ir.UnresolvedAttribute("a"))) generates "SINH(a)"
      ir.CallFunction("SIZE", Seq(ir.UnresolvedAttribute("a"))) generates "SIZE(a)"
      ir.CallFunction("SKEWNESS", Seq(ir.UnresolvedAttribute("a"))) generates "SKEWNESS(a)"

      ir.CallFunction(
        "SLICE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SLICE(a, b, c)"

      ir.CallFunction(
        "SORT_ARRAY",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SORT_ARRAY(a, b)"
      ir.CallFunction("SOUNDEX", Seq(ir.UnresolvedAttribute("a"))) generates "SOUNDEX(a)"
      ir.CallFunction("SPACE", Seq(ir.UnresolvedAttribute("a"))) generates "SPACE(a)"
      ir.CallFunction("SPARK_PARTITION_ID", Seq()) generates "SPARK_PARTITION_ID()"

      ir.CallFunction(
        "SPLIT",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SPLIT(a, b, c)"
      ir.CallFunction("SQRT", Seq(ir.UnresolvedAttribute("a"))) generates "SQRT(a)"

      ir.CallFunction("STACK", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "STACK(a, b)"
      ir.CallFunction("STD", Seq(ir.UnresolvedAttribute("a"))) generates "STD(a)"
      ir.CallFunction("STDDEV", Seq(ir.UnresolvedAttribute("a"))) generates "STDDEV(a)"
      ir.CallFunction("STDDEV_POP", Seq(ir.UnresolvedAttribute("a"))) generates "STDDEV_POP(a)"

      ir.CallFunction(
        "STR_TO_MAP",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "STR_TO_MAP(a, b, c)"

      ir.CallFunction(
        "SUBSTR",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SUBSTR(a, b, c)"

      ir.CallFunction(
        "SUBSTRING_INDEX",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SUBSTRING_INDEX(a, b, c)"
      ir.CallFunction("SUM", Seq(ir.UnresolvedAttribute("a"))) generates "SUM(a)"
      ir.CallFunction("TAN", Seq(ir.UnresolvedAttribute("a"))) generates "TAN(a)"
      ir.CallFunction("TANH", Seq(ir.UnresolvedAttribute("a"))) generates "TANH(a)"
      ir.CallFunction("TIMESTAMP_MICROS", Seq(ir.UnresolvedAttribute("a"))) generates "TIMESTAMP_MICROS(a)"
      ir.CallFunction("TIMESTAMP_MILLIS", Seq(ir.UnresolvedAttribute("a"))) generates "TIMESTAMP_MILLIS(a)"
      ir.CallFunction("TIMESTAMP_SECONDS", Seq(ir.UnresolvedAttribute("a"))) generates "TIMESTAMP_SECONDS(a)"

      ir.CallFunction("TO_CSV", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_CSV(a, b)"

      ir.CallFunction(
        "TO_DATE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_DATE(a, b)"

      ir.CallFunction(
        "TO_JSON",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_JSON(a, b)"

      ir.CallFunction(
        "TO_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_TIMESTAMP(a, b)"

      ir.CallFunction(
        "TO_UNIX_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_UNIX_TIMESTAMP(a, b)"

      ir.CallFunction(
        "TO_UTC_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_UTC_TIMESTAMP(a, b)"

      ir.CallFunction(
        "TRANSFORM",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRANSFORM(a, b)"

      ir.CallFunction(
        "TRANSFORM_KEYS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRANSFORM_KEYS(a, b)"

      ir.CallFunction(
        "TRANSFORM_VALUES",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRANSFORM_VALUES(a, b)"

      ir.CallFunction(
        "TRANSLATE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "TRANSLATE(a, b, c)"

      ir.CallFunction("TRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRIM(a, b)"

      ir.CallFunction("TRUNC", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRUNC(a, b)"
      ir.CallFunction("TYPEOF", Seq(ir.UnresolvedAttribute("a"))) generates "TYPEOF(a)"
      ir.CallFunction("UCASE", Seq(ir.UnresolvedAttribute("a"))) generates "UCASE(a)"
      ir.CallFunction("UNBASE64", Seq(ir.UnresolvedAttribute("a"))) generates "UNBASE64(a)"
      ir.CallFunction("UNHEX", Seq(ir.UnresolvedAttribute("a"))) generates "UNHEX(a)"
      ir.CallFunction("UNIX_DATE", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_DATE(a)"
      ir.CallFunction("UNIX_MICROS", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_MICROS(a)"
      ir.CallFunction("UNIX_MILLIS", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_MILLIS(a)"
      ir.CallFunction("UNIX_SECONDS", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_SECONDS(a)"

      ir.CallFunction(
        "UNIX_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "UNIX_TIMESTAMP(a, b)"
      ir.CallFunction("UUID", Seq()) generates "UUID()"
      ir.CallFunction("VAR_POP", Seq(ir.UnresolvedAttribute("a"))) generates "VAR_POP(a)"
      ir.CallFunction("VAR_SAMP", Seq(ir.UnresolvedAttribute("a"))) generates "VAR_SAMP(a)"
      ir.CallFunction("VERSION", Seq()) generates "VERSION()"
      ir.CallFunction("WEEKDAY", Seq(ir.UnresolvedAttribute("a"))) generates "WEEKDAY(a)"
      ir.CallFunction("WEEKOFYEAR", Seq(ir.UnresolvedAttribute("a"))) generates "WEEKOFYEAR(a)"

      ir.CallFunction(
        "WIDTH_BUCKET",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "WIDTH_BUCKET(a, b, c, d)"

      ir.CallFunction("XPATH", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH(a, b)"

      ir.CallFunction(
        "XPATH_BOOLEAN",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_BOOLEAN(a, b)"

      ir.CallFunction(
        "XPATH_DOUBLE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_DOUBLE(a, b)"

      ir.CallFunction(
        "XPATH_FLOAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_FLOAT(a, b)"

      ir.CallFunction(
        "XPATH_INT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_INT(a, b)"

      ir.CallFunction(
        "XPATH_LONG",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_LONG(a, b)"

      ir.CallFunction(
        "XPATH_SHORT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_SHORT(a, b)"

      ir.CallFunction(
        "XPATH_STRING",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_STRING(a, b)"

      ir.CallFunction(
        "XXHASH64",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XXHASH64(a, b)"
      ir.CallFunction("YEAR", Seq(ir.UnresolvedAttribute("a"))) generates "YEAR(a)"

      ir.CallFunction(
        "ZIP_WITH",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "ZIP_WITH(a, b, c)"
    }
  }

  "literal" should {
    "be generated" in {
      ir.Literal() generates "NULL"

      ir.Literal(binary = Some(Array(0x01, 0x02, 0x03))) generates "010203"

      ir.Literal(boolean = Some(true)) generates "TRUE"

      ir.Literal(short = Some(123)) generates "123"

      ir.Literal(integer = Some(123)) generates "123"

      ir.Literal(long = Some(123)) generates "123"

      ir.Literal(float = Some(123.4f)) generates "123.4"

      ir.Literal(double = Some(123.4)) generates "123.4"

      ir.Literal(string = Some("abc")) generates "'abc'"

      ir.Literal(date = Some(1721757801000L)) generates "'2024-07-23'"

      // we should generate UTC timezone
      //  ir.Literal(timestamp = Some(1721757801000L)) generates "\"2024-07-23 18:03:21.000\""
    }

    "arrays" in {
      ir.Literal(Seq(ir.Literal("abc"), ir.Literal("def"))) generates "ARRAY('abc', 'def')"
    }

    "maps" in {
      ir.Literal(
        Map("foo" -> ir.Literal("bar"), "baz" -> ir.Literal("qux"))) generates "MAP('foo', 'bar', 'baz', 'qux')"
    }
  }

  "distinct" should {
    "be generated" in {
      ir.Distinct(ir.Id("c1")) generates "DISTINCT c1"
    }
  }

  "star" should {
    "be generated" in {
      ir.Star(None) generates "*"
      ir.Star(Some(ir.ObjectReference(ir.Id("t1")))) generates "t1.*"
      ir.Star(
        Some(
          ir.ObjectReference(
            ir.Id("schema1"),
            ir.Id("table 1", caseSensitive = true)))) generates "schema1.\"table 1\".*"
    }
  }
}
