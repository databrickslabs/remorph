package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class ExpressionGeneratorTest extends AnyWordSpec with Matchers with MockitoSugar {
  private def generate(expr: ir.Expression): String = {
    new ExpressionGenerator().expression(new GeneratorContext(), expr)
  }

  "functions" should {
    "be generated" in {
      generate(ir.CallFunction("ABS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ABS(a)"
      generate(ir.CallFunction("ACOS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ACOS(a)"
      generate(ir.CallFunction("ACOSH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ACOSH(a)"
      generate(
        ir.CallFunction(
          "ADD_MONTHS",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ADD_MONTHS(a, b)"
      generate(
        ir.CallFunction(
          "AGGREGATE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c"),
            ir.UnresolvedAttribute("d")))) shouldBe "AGGREGATE(a, b, c, d)"
      generate(ir.CallFunction("ANY", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ANY(a)"
      generate(
        ir.CallFunction(
          "APPROX_COUNT_DISTINCT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "APPROX_COUNT_DISTINCT(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c"),
            ir.UnresolvedAttribute("d")))) shouldBe "ARRAY(a, b, c, d)"
      generate(
        ir.CallFunction(
          "ARRAYS_OVERLAP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAYS_OVERLAP(a, b)"
      generate(
        ir.CallFunction(
          "ARRAYS_ZIP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAYS_ZIP(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_CONTAINS",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_CONTAINS(a, b)"
      generate(ir.CallFunction("ARRAY_DISTINCT", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ARRAY_DISTINCT(a)"
      generate(
        ir.CallFunction(
          "ARRAY_EXCEPT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_EXCEPT(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_INTERSECT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_INTERSECT(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_JOIN",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "ARRAY_JOIN(a, b, c)"
      generate(ir.CallFunction("ARRAY_MAX", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ARRAY_MAX(a)"
      generate(ir.CallFunction("ARRAY_MIN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ARRAY_MIN(a)"
      generate(
        ir.CallFunction(
          "ARRAY_POSITION",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_POSITION(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_REMOVE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_REMOVE(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_REPEAT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_REPEAT(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_SORT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_SORT(a, b)"
      generate(
        ir.CallFunction(
          "ARRAY_UNION",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ARRAY_UNION(a, b)"
      generate(ir.CallFunction("ASCII", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ASCII(a)"
      generate(ir.CallFunction("ASIN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ASIN(a)"
      generate(ir.CallFunction("ASINH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ASINH(a)"
      generate(
        ir.CallFunction(
          "ASSERT_TRUE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ASSERT_TRUE(a, b)"
      generate(ir.CallFunction("ATAN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ATAN(a)"
      generate(
        ir.CallFunction("ATAN2", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ATAN2(a, b)"
      generate(ir.CallFunction("ATANH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ATANH(a)"
      generate(ir.CallFunction("AVG", Seq(ir.UnresolvedAttribute("a")))) shouldBe "AVG(a)"
      generate(ir.CallFunction("BASE64", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BASE64(a)"
      generate(ir.CallFunction("BIN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BIN(a)"
      generate(ir.CallFunction("BIT_AND", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BIT_AND(a)"
      generate(ir.CallFunction("BIT_COUNT", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BIT_COUNT(a)"
      generate(ir.CallFunction("BIT_LENGTH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BIT_LENGTH(a)"
      generate(ir.CallFunction("BIT_OR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BIT_OR(a)"
      generate(ir.CallFunction("BIT_XOR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BIT_XOR(a)"
      generate(ir.CallFunction("BOOL_AND", Seq(ir.UnresolvedAttribute("a")))) shouldBe "BOOL_AND(a)"
      generate(
        ir.CallFunction(
          "BROUND",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "BROUND(a, b)"
      generate(ir.CallFunction("CBRT", Seq(ir.UnresolvedAttribute("a")))) shouldBe "CBRT(a)"
      generate(ir.CallFunction("CEIL", Seq(ir.UnresolvedAttribute("a")))) shouldBe "CEIL(a)"
      generate(ir.CallFunction("CHAR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "CHAR(a)"
      generate(
        ir.CallFunction(
          "COALESCE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "COALESCE(a, b)"
      generate(ir.CallFunction("COLLECT_LIST", Seq(ir.UnresolvedAttribute("a")))) shouldBe "COLLECT_LIST(a)"
      generate(ir.CallFunction("COLLECT_SET", Seq(ir.UnresolvedAttribute("a")))) shouldBe "COLLECT_SET(a)"
      generate(
        ir.CallFunction(
          "CONCAT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "CONCAT(a, b)"
      generate(
        ir.CallFunction(
          "CONCAT_WS",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "CONCAT_WS(a, b)"
      generate(
        ir.CallFunction(
          "CONV",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "CONV(a, b, c)"
      generate(
        ir.CallFunction("CORR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "CORR(a, b)"
      generate(ir.CallFunction("COS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "COS(a)"
      generate(ir.CallFunction("COSH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "COSH(a)"
      generate(ir.CallFunction("COT", Seq(ir.UnresolvedAttribute("a")))) shouldBe "COT(a)"
      generate(
        ir.CallFunction("COUNT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "COUNT(a, b)"
      generate(ir.CallFunction("COUNT_IF", Seq(ir.UnresolvedAttribute("a")))) shouldBe "COUNT_IF(a)"
      generate(
        ir.CallFunction(
          "COUNT_MIN_SKETCH",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c"),
            ir.UnresolvedAttribute("d")))) shouldBe "COUNT_MIN_SKETCH(a, b, c, d)"
      generate(
        ir.CallFunction(
          "COVAR_POP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "COVAR_POP(a, b)"
      generate(
        ir.CallFunction(
          "COVAR_SAMP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "COVAR_SAMP(a, b)"
      generate(ir.CallFunction("CRC32", Seq(ir.UnresolvedAttribute("a")))) shouldBe "CRC32(a)"
      generate(
        ir.CallFunction("CUBE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "CUBE(a, b)"
      generate(ir.CallFunction("CUME_DIST", Seq())) shouldBe "CUME_DIST()"
      generate(ir.CallFunction("CURRENT_CATALOG", Seq())) shouldBe "CURRENT_CATALOG()"
      generate(ir.CallFunction("CURRENT_DATABASE", Seq())) shouldBe "CURRENT_DATABASE()"
      generate(ir.CallFunction("CURRENT_DATE", Seq())) shouldBe "CURRENT_DATE()"
      generate(ir.CallFunction("CURRENT_TIMESTAMP", Seq())) shouldBe "CURRENT_TIMESTAMP()"
      generate(ir.CallFunction("CURRENT_TIMEZONE", Seq())) shouldBe "CURRENT_TIMEZONE()"
      generate(
        ir.CallFunction(
          "DATEDIFF",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DATEDIFF(a, b)"
      generate(
        ir.CallFunction(
          "DATE_ADD",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DATE_ADD(a, b)"
      generate(
        ir.CallFunction(
          "DATE_FORMAT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DATE_FORMAT(a, b)"
      generate(
        ir.CallFunction("DATE_FROM_UNIX_DATE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "DATE_FROM_UNIX_DATE(a)"
      generate(
        ir.CallFunction(
          "DATE_PART",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DATE_PART(a, b)"
      generate(
        ir.CallFunction(
          "DATE_SUB",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DATE_SUB(a, b)"
      generate(
        ir.CallFunction(
          "DATE_TRUNC",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DATE_TRUNC(a, b)"
      generate(ir.CallFunction("DAYOFMONTH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "DAYOFMONTH(a)"
      generate(ir.CallFunction("DAYOFWEEK", Seq(ir.UnresolvedAttribute("a")))) shouldBe "DAYOFWEEK(a)"
      generate(ir.CallFunction("DAYOFYEAR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "DAYOFYEAR(a)"
      generate(
        ir.CallFunction(
          "DECODE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DECODE(a, b)"
      generate(ir.CallFunction("DEGREES", Seq(ir.UnresolvedAttribute("a")))) shouldBe "DEGREES(a)"
      generate(
        ir.CallFunction(
          "DENSE_RANK",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DENSE_RANK(a, b)"
      generate(
        ir.CallFunction("DIV", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "DIV(a, b)"
      generate(ir.CallFunction("E", Seq())) shouldBe "E()"
      generate(
        ir.CallFunction(
          "ELEMENT_AT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ELEMENT_AT(a, b)"
      generate(
        ir.CallFunction("ELT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ELT(a, b)"
      generate(
        ir.CallFunction(
          "ENCODE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ENCODE(a, b)"
      generate(
        ir.CallFunction(
          "EXISTS",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "EXISTS(a, b)"
      generate(ir.CallFunction("EXP", Seq(ir.UnresolvedAttribute("a")))) shouldBe "EXP(a)"
      generate(ir.CallFunction("EXPLODE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "EXPLODE(a)"
      generate(ir.CallFunction("EXPM1", Seq(ir.UnresolvedAttribute("a")))) shouldBe "EXPM1(a)"
      generate(
        ir.CallFunction(
          "EXTRACT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "EXTRACT(a, b)"
      generate(ir.CallFunction("FACTORIAL", Seq(ir.UnresolvedAttribute("a")))) shouldBe "FACTORIAL(a)"
      generate(
        ir.CallFunction(
          "FILTER",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FILTER(a, b)"
      generate(
        ir.CallFunction(
          "FIND_IN_SET",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FIND_IN_SET(a, b)"
      generate(
        ir.CallFunction("FIRST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FIRST(a, b)"
      generate(ir.CallFunction("FLATTEN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "FLATTEN(a)"
      generate(ir.CallFunction("FLOOR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "FLOOR(a)"
      generate(
        ir.CallFunction(
          "FORALL",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FORALL(a, b)"
      generate(
        ir.CallFunction(
          "FORMAT_NUMBER",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FORMAT_NUMBER(a, b)"
      generate(
        ir.CallFunction(
          "FORMAT_STRING",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FORMAT_STRING(a, b)"
      generate(
        ir.CallFunction(
          "FROM_CSV",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "FROM_CSV(a, b, c)"
      generate(
        ir.CallFunction(
          "FROM_JSON",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "FROM_JSON(a, b, c)"
      generate(
        ir.CallFunction(
          "FROM_UNIXTIME",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FROM_UNIXTIME(a, b)"
      generate(
        ir.CallFunction(
          "FROM_UTC_TIMESTAMP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "FROM_UTC_TIMESTAMP(a, b)"
      generate(
        ir.CallFunction(
          "GET_JSON_OBJECT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "GET_JSON_OBJECT(a, b)"
      generate(
        ir.CallFunction(
          "GREATEST",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "GREATEST(a, b)"
      generate(ir.CallFunction("GROUPING", Seq(ir.UnresolvedAttribute("a")))) shouldBe "GROUPING(a)"
      generate(
        ir.CallFunction(
          "GROUPING_ID",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "GROUPING_ID(a, b)"
      generate(
        ir.CallFunction("HASH", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "HASH(a, b)"
      generate(ir.CallFunction("HEX", Seq(ir.UnresolvedAttribute("a")))) shouldBe "HEX(a)"
      generate(ir.CallFunction("HOUR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "HOUR(a)"
      generate(
        ir.CallFunction("HYPOT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "HYPOT(a, b)"
      generate(
        ir.CallFunction(
          "IF",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "IF(a, b, c)"
      generate(
        ir.CallFunction(
          "IFNULL",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "IFNULL(a, b)"
      generate(ir.CallFunction("INITCAP", Seq(ir.UnresolvedAttribute("a")))) shouldBe "INITCAP(a)"
      generate(ir.CallFunction("INLINE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "INLINE(a)"
      generate(ir.CallFunction("INPUT_FILE_BLOCK_LENGTH", Seq())) shouldBe "INPUT_FILE_BLOCK_LENGTH()"
      generate(ir.CallFunction("INPUT_FILE_BLOCK_START", Seq())) shouldBe "INPUT_FILE_BLOCK_START()"
      generate(ir.CallFunction("INPUT_FILE_NAME", Seq())) shouldBe "INPUT_FILE_NAME()"
      generate(
        ir.CallFunction("INSTR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "INSTR(a, b)"
      generate(ir.CallFunction("ISNAN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ISNAN(a)"
      generate(ir.CallFunction("ISNOTNULL", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ISNOTNULL(a)"
      generate(ir.CallFunction("ISNULL", Seq(ir.UnresolvedAttribute("a")))) shouldBe "ISNULL(a)"
      generate(
        ir.CallFunction(
          "JAVA_METHOD",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "JAVA_METHOD(a, b)"
      generate(ir.CallFunction("JSON_ARRAY_LENGTH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "JSON_ARRAY_LENGTH(a)"
      generate(ir.CallFunction("JSON_OBJECT_KEYS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "JSON_OBJECT_KEYS(a)"
      generate(
        ir.CallFunction(
          "JSON_TUPLE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "JSON_TUPLE(a, b)"
      generate(ir.CallFunction("KURTOSIS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "KURTOSIS(a)"
      generate(
        ir.CallFunction(
          "LAG",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "LAG(a, b, c)"
      generate(
        ir.CallFunction("LAST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "LAST(a, b)"
      generate(ir.CallFunction("LAST_DAY", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LAST_DAY(a)"
      generate(
        ir.CallFunction(
          "LEAD",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "LEAD(a, b, c)"
      generate(
        ir.CallFunction("LEAST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "LEAST(a, b)"
      generate(
        ir.CallFunction("LEFT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "LEFT(a, b)"
      generate(ir.CallFunction("LENGTH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LENGTH(a)"
      generate(
        ir.CallFunction(
          "LEVENSHTEIN",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "LEVENSHTEIN(a, b)"
      generate(ir.CallFunction("LN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LN(a)"
      generate(
        ir.CallFunction("LOG", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "LOG(a, b)"
      generate(ir.CallFunction("LOG10", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LOG10(a)"
      generate(ir.CallFunction("LOG1P", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LOG1P(a)"
      generate(ir.CallFunction("LOG2", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LOG2(a)"
      generate(ir.CallFunction("LOWER", Seq(ir.UnresolvedAttribute("a")))) shouldBe "LOWER(a)"
      generate(
        ir.CallFunction("LTRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "LTRIM(a, b)"
      generate(
        ir.CallFunction(
          "MAKE_DATE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "MAKE_DATE(a, b, c)"
      generate(
        ir.CallFunction(
          "MAP_CONCAT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "MAP_CONCAT(a, b)"
      generate(ir.CallFunction("MAP_ENTRIES", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MAP_ENTRIES(a)"
      generate(
        ir.CallFunction(
          "MAP_FILTER",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "MAP_FILTER(a, b)"
      generate(
        ir.CallFunction(
          "MAP_FROM_ARRAYS",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "MAP_FROM_ARRAYS(a, b)"
      generate(ir.CallFunction("MAP_FROM_ENTRIES", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MAP_FROM_ENTRIES(a)"
      generate(ir.CallFunction("MAP_KEYS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MAP_KEYS(a)"
      generate(ir.CallFunction("MAP_VALUES", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MAP_VALUES(a)"
      generate(
        ir.CallFunction(
          "MAP_ZIP_WITH",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "MAP_ZIP_WITH(a, b, c)"
      generate(ir.CallFunction("MAX", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MAX(a)"
      generate(
        ir.CallFunction(
          "MAX_BY",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "MAX_BY(a, b)"
      generate(ir.CallFunction("MD5", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MD5(a)"
      generate(ir.CallFunction("MIN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MIN(a)"
      generate(ir.CallFunction("MINUTE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MINUTE(a)"
      generate(
        ir.CallFunction(
          "MIN_BY",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "MIN_BY(a, b)"
      generate(
        ir.CallFunction("MOD", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "MOD(a, b)"
      generate(ir.CallFunction("MONOTONICALLY_INCREASING_ID", Seq())) shouldBe "MONOTONICALLY_INCREASING_ID()"
      generate(ir.CallFunction("MONTH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "MONTH(a)"
      generate(
        ir.CallFunction(
          "MONTHS_BETWEEN",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "MONTHS_BETWEEN(a, b, c)"
      generate(
        ir.CallFunction(
          "NAMED_STRUCT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "NAMED_STRUCT(a, b)"
      generate(
        ir.CallFunction("NANVL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "NANVL(a, b)"
      generate(ir.CallFunction("NEGATIVE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "NEGATIVE(a)"
      generate(
        ir.CallFunction(
          "NEXT_DAY",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "NEXT_DAY(a, b)"
      generate(ir.CallFunction("NOW", Seq())) shouldBe "NOW()"
      generate(
        ir.CallFunction(
          "NTH_VALUE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "NTH_VALUE(a, b)"
      generate(ir.CallFunction("NTILE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "NTILE(a)"
      generate(
        ir.CallFunction(
          "NULLIF",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "NULLIF(a, b)"
      generate(
        ir.CallFunction("NVL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "NVL(a, b)"
      generate(
        ir.CallFunction(
          "NVL2",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "NVL2(a, b, c)"
      generate(ir.CallFunction("OCTET_LENGTH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "OCTET_LENGTH(a)"
      generate(ir.CallFunction("OR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "OR(a, b)"
      generate(
        ir.CallFunction(
          "OVERLAY",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c"),
            ir.UnresolvedAttribute("d")))) shouldBe "OVERLAY(a, b, c, d)"
      generate(
        ir.CallFunction(
          "PARSE_URL",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "PARSE_URL(a, b)"
      generate(
        ir.CallFunction(
          "PERCENTILE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "PERCENTILE(a, b, c)"
      generate(
        ir.CallFunction(
          "PERCENTILE_APPROX",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "PERCENTILE_APPROX(a, b, c)"
      generate(
        ir.CallFunction(
          "PERCENT_RANK",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "PERCENT_RANK(a, b)"
      generate(ir.CallFunction("PI", Seq())) shouldBe "PI()"
      generate(
        ir.CallFunction("PMOD", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "PMOD(a, b)"
      generate(ir.CallFunction("POSEXPLODE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "POSEXPLODE(a)"
      generate(ir.CallFunction("POSITIVE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "POSITIVE(a)"
      generate(
        ir.CallFunction("POW", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "POW(a, b)"
      generate(ir.CallFunction("QUARTER", Seq(ir.UnresolvedAttribute("a")))) shouldBe "QUARTER(a)"
      generate(ir.CallFunction("RADIANS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "RADIANS(a)"
      generate(ir.CallFunction("RAISE_ERROR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "RAISE_ERROR(a)"
      generate(ir.CallFunction("RAND", Seq(ir.UnresolvedAttribute("a")))) shouldBe "RAND(a)"
      generate(ir.CallFunction("RANDN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "RANDN(a)"
      generate(
        ir.CallFunction("RANK", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "RANK(a, b)"
      generate(
        ir.CallFunction(
          "REGEXP_EXTRACT",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "REGEXP_EXTRACT(a, b, c)"
      generate(
        ir.CallFunction(
          "REGEXP_EXTRACT_ALL",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "REGEXP_EXTRACT_ALL(a, b, c)"
      generate(
        ir.CallFunction(
          "REGEXP_REPLACE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c"),
            ir.UnresolvedAttribute("d")))) shouldBe "REGEXP_REPLACE(a, b, c, d)"
      generate(
        ir.CallFunction(
          "REPEAT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "REPEAT(a, b)"
      generate(
        ir.CallFunction(
          "REPLACE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "REPLACE(a, b, c)"
      generate(ir.CallFunction("REVERSE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "REVERSE(a)"
      generate(
        ir.CallFunction("RIGHT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "RIGHT(a, b)"
      generate(ir.CallFunction("RINT", Seq(ir.UnresolvedAttribute("a")))) shouldBe "RINT(a)"
      generate(
        ir.CallFunction("RLIKE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "RLIKE(a, b)"
      generate(
        ir.CallFunction(
          "ROLLUP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ROLLUP(a, b)"
      generate(
        ir.CallFunction("ROUND", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "ROUND(a, b)"
      generate(ir.CallFunction("ROW_NUMBER", Seq())) shouldBe "ROW_NUMBER()"
      generate(
        ir.CallFunction(
          "RPAD",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "RPAD(a, b, c)"
      generate(
        ir.CallFunction("RTRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "RTRIM(a, b)"
      generate(
        ir.CallFunction(
          "SCHEMA_OF_CSV",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SCHEMA_OF_CSV(a, b)"
      generate(
        ir.CallFunction(
          "SCHEMA_OF_JSON",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SCHEMA_OF_JSON(a, b)"
      generate(ir.CallFunction("SECOND", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SECOND(a)"
      generate(
        ir.CallFunction(
          "SENTENCES",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "SENTENCES(a, b, c)"
      generate(
        ir.CallFunction(
          "SEQUENCE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "SEQUENCE(a, b, c)"
      generate(ir.CallFunction("SHA", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SHA(a)"
      generate(
        ir.CallFunction("SHA2", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SHA2(a, b)"
      generate(
        ir.CallFunction(
          "SHIFTLEFT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SHIFTLEFT(a, b)"
      generate(
        ir.CallFunction(
          "SHIFTRIGHT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SHIFTRIGHT(a, b)"
      generate(
        ir.CallFunction(
          "SHIFTRIGHTUNSIGNED",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SHIFTRIGHTUNSIGNED(a, b)"
      generate(ir.CallFunction("SHUFFLE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SHUFFLE(a)"
      generate(ir.CallFunction("SIGN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SIGN(a)"
      generate(ir.CallFunction("SIN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SIN(a)"
      generate(ir.CallFunction("SINH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SINH(a)"
      generate(ir.CallFunction("SIZE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SIZE(a)"
      generate(ir.CallFunction("SKEWNESS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SKEWNESS(a)"
      generate(
        ir.CallFunction(
          "SLICE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "SLICE(a, b, c)"
      generate(
        ir.CallFunction(
          "SORT_ARRAY",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "SORT_ARRAY(a, b)"
      generate(ir.CallFunction("SOUNDEX", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SOUNDEX(a)"
      generate(ir.CallFunction("SPACE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SPACE(a)"
      generate(ir.CallFunction("SPARK_PARTITION_ID", Seq())) shouldBe "SPARK_PARTITION_ID()"
      generate(
        ir.CallFunction(
          "SPLIT",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "SPLIT(a, b, c)"
      generate(ir.CallFunction("SQRT", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SQRT(a)"
      generate(
        ir.CallFunction("STACK", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "STACK(a, b)"
      generate(ir.CallFunction("STD", Seq(ir.UnresolvedAttribute("a")))) shouldBe "STD(a)"
      generate(ir.CallFunction("STDDEV", Seq(ir.UnresolvedAttribute("a")))) shouldBe "STDDEV(a)"
      generate(ir.CallFunction("STDDEV_POP", Seq(ir.UnresolvedAttribute("a")))) shouldBe "STDDEV_POP(a)"
      generate(
        ir.CallFunction(
          "STR_TO_MAP",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "STR_TO_MAP(a, b, c)"
      generate(
        ir.CallFunction(
          "SUBSTR",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "SUBSTR(a, b, c)"
      generate(
        ir.CallFunction(
          "SUBSTRING_INDEX",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "SUBSTRING_INDEX(a, b, c)"
      generate(ir.CallFunction("SUM", Seq(ir.UnresolvedAttribute("a")))) shouldBe "SUM(a)"
      generate(ir.CallFunction("TAN", Seq(ir.UnresolvedAttribute("a")))) shouldBe "TAN(a)"
      generate(ir.CallFunction("TANH", Seq(ir.UnresolvedAttribute("a")))) shouldBe "TANH(a)"
      generate(ir.CallFunction("TIMESTAMP_MICROS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "TIMESTAMP_MICROS(a)"
      generate(ir.CallFunction("TIMESTAMP_MILLIS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "TIMESTAMP_MILLIS(a)"
      generate(ir.CallFunction("TIMESTAMP_SECONDS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "TIMESTAMP_SECONDS(a)"
      generate(
        ir.CallFunction(
          "TO_CSV",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TO_CSV(a, b)"
      generate(
        ir.CallFunction(
          "TO_DATE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TO_DATE(a, b)"
      generate(
        ir.CallFunction(
          "TO_JSON",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TO_JSON(a, b)"
      generate(
        ir.CallFunction(
          "TO_TIMESTAMP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TO_TIMESTAMP(a, b)"
      generate(
        ir.CallFunction(
          "TO_UNIX_TIMESTAMP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TO_UNIX_TIMESTAMP(a, b)"
      generate(
        ir.CallFunction(
          "TO_UTC_TIMESTAMP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TO_UTC_TIMESTAMP(a, b)"
      generate(
        ir.CallFunction(
          "TRANSFORM",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TRANSFORM(a, b)"
      generate(
        ir.CallFunction(
          "TRANSFORM_KEYS",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TRANSFORM_KEYS(a, b)"
      generate(
        ir.CallFunction(
          "TRANSFORM_VALUES",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TRANSFORM_VALUES(a, b)"
      generate(
        ir.CallFunction(
          "TRANSLATE",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "TRANSLATE(a, b, c)"
      generate(
        ir.CallFunction("TRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TRIM(a, b)"
      generate(
        ir.CallFunction("TRUNC", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "TRUNC(a, b)"
      generate(ir.CallFunction("TYPEOF", Seq(ir.UnresolvedAttribute("a")))) shouldBe "TYPEOF(a)"
      generate(ir.CallFunction("UCASE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UCASE(a)"
      generate(ir.CallFunction("UNBASE64", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UNBASE64(a)"
      generate(ir.CallFunction("UNHEX", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UNHEX(a)"
      generate(ir.CallFunction("UNIX_DATE", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UNIX_DATE(a)"
      generate(ir.CallFunction("UNIX_MICROS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UNIX_MICROS(a)"
      generate(ir.CallFunction("UNIX_MILLIS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UNIX_MILLIS(a)"
      generate(ir.CallFunction("UNIX_SECONDS", Seq(ir.UnresolvedAttribute("a")))) shouldBe "UNIX_SECONDS(a)"
      generate(
        ir.CallFunction(
          "UNIX_TIMESTAMP",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "UNIX_TIMESTAMP(a, b)"
      generate(ir.CallFunction("UUID", Seq())) shouldBe "UUID()"
      generate(ir.CallFunction("VAR_POP", Seq(ir.UnresolvedAttribute("a")))) shouldBe "VAR_POP(a)"
      generate(ir.CallFunction("VAR_SAMP", Seq(ir.UnresolvedAttribute("a")))) shouldBe "VAR_SAMP(a)"
      generate(ir.CallFunction("VERSION", Seq())) shouldBe "VERSION()"
      generate(ir.CallFunction("WEEKDAY", Seq(ir.UnresolvedAttribute("a")))) shouldBe "WEEKDAY(a)"
      generate(ir.CallFunction("WEEKOFYEAR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "WEEKOFYEAR(a)"
      generate(
        ir.CallFunction(
          "WIDTH_BUCKET",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c"),
            ir.UnresolvedAttribute("d")))) shouldBe "WIDTH_BUCKET(a, b, c, d)"
      generate(
        ir.CallFunction("XPATH", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_BOOLEAN",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_BOOLEAN(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_DOUBLE",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_DOUBLE(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_FLOAT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_FLOAT(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_INT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_INT(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_LONG",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_LONG(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_SHORT",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_SHORT(a, b)"
      generate(
        ir.CallFunction(
          "XPATH_STRING",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XPATH_STRING(a, b)"
      generate(
        ir.CallFunction(
          "XXHASH64",
          Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")))) shouldBe "XXHASH64(a, b)"
      generate(ir.CallFunction("YEAR", Seq(ir.UnresolvedAttribute("a")))) shouldBe "YEAR(a)"
      generate(
        ir.CallFunction(
          "ZIP_WITH",
          Seq(
            ir.UnresolvedAttribute("a"),
            ir.UnresolvedAttribute("b"),
            ir.UnresolvedAttribute("c")))) shouldBe "ZIP_WITH(a, b, c)"
    }
  }

  "literal" should {
    "be generated" in {
      generate(ir.Literal()) shouldBe "NULL"

      generate(ir.Literal(binary = Some(Array(0x01, 0x02, 0x03)))) shouldBe "010203"

      generate(ir.Literal(boolean = Some(true))) shouldBe "TRUE"

      generate(ir.Literal(short = Some(123))) shouldBe "123"

      generate(ir.Literal(integer = Some(123))) shouldBe "123"

      generate(ir.Literal(long = Some(123))) shouldBe "123"

      generate(ir.Literal(float = Some(123.4f))) shouldBe "123.4"

      generate(ir.Literal(double = Some(123.4))) shouldBe "123.4"

      generate(ir.Literal(string = Some("abc"))) shouldBe "\"abc\""

      generate(ir.Literal(date = Some(1721757801000L))) shouldBe "\"2024-07-23\""

      // we should generate UTC timezone
      // generate(ir.Literal(timestamp = Some(1721757801000L))) shouldBe "\"2024-07-23 18:03:21.000\""
    }

    "arrays" in {
      generate(ir.Literal(Seq(ir.Literal("abc"), ir.Literal("def")))) shouldBe "ARRAY(\"abc\", \"def\")"
    }

    "maps" in {
      generate(
        ir.Literal(
          Map(
            "foo" -> ir.Literal("bar"),
            "baz" -> ir.Literal("qux")))) shouldBe "MAP(\"foo\", \"bar\", \"baz\", \"qux\")"
    }
  }
}
