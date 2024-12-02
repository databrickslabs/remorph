package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{GeneratorContext, GeneratorTestCommon}
import com.databricks.labs.remorph.{Generating, intermediate => ir}
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

import java.sql.{Date, Timestamp}

class ExpressionGeneratorTest
    extends AnyWordSpec
    with GeneratorTestCommon[ir.Expression]
    with MockitoSugar
    with ir.IRHelpers {

  override protected val generator = new ExpressionGenerator

  private val optionGenerator = new OptionGenerator(generator)

  private val logical = new LogicalPlanGenerator(generator, optionGenerator)

  override protected def initialState(expr: ir.Expression) =
    Generating(optimizedPlan = ir.Batch(Seq.empty), currentNode = expr, ctx = GeneratorContext(logical))

  "options" in {
    ir.Options(
      Map(
        "KEEPFIXED" -> ir.Column(None, ir.Id("PLAN")),
        "FAST" -> ir.Literal(666),
        "MAX_GRANT_PERCENT" -> ir.Literal(30)),
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

  "struct" in {
    ir.StructExpr(
      Seq(
        ir.Alias(ir.Literal(1), ir.Id("a")),
        ir.Alias(ir.Literal("two"), ir.Id("b")),
        ir.Alias(ir.Literal(Seq(1, 2, 3)), ir.Id("c")))) generates "STRUCT(1 AS a, 'two' AS b, ARRAY(1, 2, 3) AS c)"
  }

  "columns" should {
    "unresolved" in {
      ir.UnresolvedAttribute("a") generates "a"
    }
    "a" in {
      ir.Column(None, ir.Id("a")) generates "a"
    }
    "t.a" in {
      ir.Column(Some(ir.ObjectReference(ir.Id("t"))), ir.Id("a")) generates "t.a"
    }
    "s.t.a" in {
      ir.Column(Some(ir.ObjectReference(ir.Id("s.t"))), ir.Id("a")) generates "s.t.a"
    }

    "$1" in {
      ir.Column(None, ir.Position(1)).doesNotTranspile
    }
  }

  "arithmetic" should {
    "-a" in {
      ir.UMinus(ir.UnresolvedAttribute("a")) generates "-a"
    }
    "+a" in {
      ir.UPlus(ir.UnresolvedAttribute("a")) generates "+a"
    }
    "a * b" in {
      ir.Multiply(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a * b"
    }
    "a / b" in {
      ir.Divide(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a / b"
    }
    "a % b" in {
      ir.Mod(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a % b"
    }
    "a + b" in {
      ir.Add(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a + b"
    }
    "a - b" in {
      ir.Subtract(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a - b"
    }
  }

  "bitwise" should {
    "a | b" in {
      ir.BitwiseOr(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a | b"
    }
    "a & b" in {
      ir.BitwiseAnd(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a & b"
    }
    "a ^ b" in {
      ir.BitwiseXor(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a ^ b"
    }
    "~a" in {
      ir.BitwiseNot(ir.UnresolvedAttribute("a")) generates "~a"
    }
  }

  "like" should {
    "a LIKE 'b%'" in {
      ir.Like(ir.UnresolvedAttribute("a"), ir.Literal("b%"), None) generates "a LIKE 'b%'"
    }
    "a LIKE b ESCAPE '/'" in {
      ir.Like(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"), Some(ir.Literal('/'))) generates
        "a LIKE b ESCAPE '/'"
    }
    "a ILIKE 'b%'" in {
      ir.ILike(ir.UnresolvedAttribute("a"), ir.Literal("b%"), None) generates "a ILIKE 'b%'"
    }
    "a ILIKE b ESCAPE '/'" in {
      ir.ILike(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"), Some(ir.Literal('/'))) generates
        "a ILIKE b ESCAPE '/'"
    }
    "a LIKE ANY ('b%', 'c%')" in {
      ir.LikeAny(
        ir.UnresolvedAttribute("a"),
        Seq(ir.Literal("b%"), ir.Literal("c%"))) generates "a LIKE ANY ('b%', 'c%')"
    }
    "a LIKE ALL ('b%', '%c')" in {
      ir.LikeAll(
        ir.UnresolvedAttribute("a"),
        Seq(ir.Literal("b%"), ir.Literal("%c"))) generates "a LIKE ALL ('b%', '%c')"
    }
    "other ilike" in {
      ir.ILikeAny(
        ir.UnresolvedAttribute("a"),
        Seq(ir.Literal("b%"), ir.Literal("c%"))) generates "a ILIKE ANY ('b%', 'c%')"
      ir.ILikeAll(
        ir.UnresolvedAttribute("a"),
        Seq(ir.Literal("b%"), ir.Literal("%c"))) generates "a ILIKE ALL ('b%', '%c')"
    }
  }

  "predicates" should {
    "a AND b" in {
      ir.And(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a AND b"
    }
    "a OR b" in {
      ir.Or(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a OR b"
    }
    "NOT (a)" in {
      ir.Not(ir.UnresolvedAttribute("a")) generates "NOT (a)"
    }
    "a = b" in {
      ir.Equals(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a = b"
    }
    "a != b" in {
      ir.NotEquals(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a != b"
    }
    "a < b" in {
      ir.LessThan(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a < b"
    }
    "a <= b" in {
      ir.LessThanOrEqual(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a <= b"
    }
    "a > b" in {
      ir.GreaterThan(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a > b"
    }
    "a >= b" in {
      ir.GreaterThanOrEqual(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a >= b"
    }
  }

  "functions" should {
    "ABS(a)" in {
      ir.CallFunction("ABS", Seq(ir.UnresolvedAttribute("a"))) generates "ABS(a)"
    }

    "ACOS(a)" in {
      ir.CallFunction("ACOS", Seq(ir.UnresolvedAttribute("a"))) generates "ACOS(a)"
    }

    "ACOSH(a)" in {
      ir.CallFunction("ACOSH", Seq(ir.UnresolvedAttribute("a"))) generates "ACOSH(a)"
    }

    "ADD_MONTHS(a, b)" in {
      ir.CallFunction(
        "ADD_MONTHS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ADD_MONTHS(a, b)"
    }

    "AGGREGATE(a, b, c, d)" in {
      ir.CallFunction(
        "AGGREGATE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "AGGREGATE(a, b, c, d)"
    }

    "ANY(a)" in {
      ir.CallFunction("ANY", Seq(ir.UnresolvedAttribute("a"))) generates "ANY(a)"
    }

    "APPROX_COUNT_DISTINCT(a, b)" in {
      ir.CallFunction(
        "APPROX_COUNT_DISTINCT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "APPROX_COUNT_DISTINCT(a, b)"
    }

    "ARRAY(a, b, c, d)" in {
      ir.CallFunction(
        "ARRAY",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "ARRAY(a, b, c, d)"
    }

    "ARRAYS_OVERLAP(a, b)" in {
      ir.CallFunction(
        "ARRAYS_OVERLAP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAYS_OVERLAP(a, b)"
    }

    "ARRAYS_ZIP(a, b)" in {
      ir.CallFunction(
        "ARRAYS_ZIP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAYS_ZIP(a, b)"
    }

    "ARRAY_CONTAINS(a, b)" in {
      ir.CallFunction(
        "ARRAY_CONTAINS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_CONTAINS(a, b)"
    }

    "ARRAY_DISTINCT(a)" in {
      ir.CallFunction("ARRAY_DISTINCT", Seq(ir.UnresolvedAttribute("a"))) generates "ARRAY_DISTINCT(a)"
    }

    "ARRAY_EXCEPT(a, b)" in {
      ir.CallFunction(
        "ARRAY_EXCEPT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_EXCEPT(a, b)"
    }

    "ARRAY_INTERSECT(a, b)" in {
      ir.CallFunction(
        "ARRAY_INTERSECT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_INTERSECT(a, b)"
    }

    "ARRAY_JOIN(a, b, c)" in {
      ir.CallFunction(
        "ARRAY_JOIN",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "ARRAY_JOIN(a, b, c)"
    }

    "ARRAY_MAX(a)" in {
      ir.CallFunction("ARRAY_MAX", Seq(ir.UnresolvedAttribute("a"))) generates "ARRAY_MAX(a)"
    }

    "ARRAY_MIN(a)" in {
      ir.CallFunction("ARRAY_MIN", Seq(ir.UnresolvedAttribute("a"))) generates "ARRAY_MIN(a)"
    }

    "ARRAY_POSITION(a, b)" in {
      ir.CallFunction(
        "ARRAY_POSITION",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_POSITION(a, b)"
    }

    "ARRAY_REMOVE(a, b)" in {
      ir.CallFunction(
        "ARRAY_REMOVE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_REMOVE(a, b)"
    }

    "ARRAY_REMOVE([2, 3, 4::DOUBLE, 4, NULL], 4)" in {
      ir.CallFunction(
        "ARRAY_REMOVE",
        Seq(
          ir.ArrayExpr(
            Seq(ir.Literal(2), ir.Literal(3), ir.Cast(ir.Literal(4), ir.DoubleType), ir.Literal(4), ir.Literal(null)),
            ir.IntegerType),
          ir.Literal(4))) generates "ARRAY_REMOVE(ARRAY(2, 3, CAST(4 AS DOUBLE), 4, NULL), 4)"
    }

    "ARRAY_REPEAT(a, b)" in {
      ir.CallFunction(
        "ARRAY_REPEAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_REPEAT(a, b)"
    }

    "ARRAY_SORT(a, b)" in {
      ir.CallFunction(
        "ARRAY_SORT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_SORT(a, b)"
    }

    "ARRAY_UNION(a, b)" in {
      ir.CallFunction(
        "ARRAY_UNION",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ARRAY_UNION(a, b)"
    }

    "ASCII(a)" in {
      ir.CallFunction("ASCII", Seq(ir.UnresolvedAttribute("a"))) generates "ASCII(a)"
    }

    "ASIN(a)" in {
      ir.CallFunction("ASIN", Seq(ir.UnresolvedAttribute("a"))) generates "ASIN(a)"
    }

    "ASINH(a)" in {
      ir.CallFunction("ASINH", Seq(ir.UnresolvedAttribute("a"))) generates "ASINH(a)"
    }

    "ASSERT_TRUE(a, b)" in {
      ir.CallFunction(
        "ASSERT_TRUE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ASSERT_TRUE(a, b)"
    }

    "ATAN(a)" in {
      ir.CallFunction("ATAN", Seq(ir.UnresolvedAttribute("a"))) generates "ATAN(a)"
    }

    "ATAN2(a, b)" in {
      ir.CallFunction("ATAN2", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ATAN2(a, b)"
    }

    "ATANH(a)" in {
      ir.CallFunction("ATANH", Seq(ir.UnresolvedAttribute("a"))) generates "ATANH(a)"
    }

    "AVG(a)" in {
      ir.CallFunction("AVG", Seq(ir.UnresolvedAttribute("a"))) generates "AVG(a)"
    }

    "BASE64(a)" in {
      ir.CallFunction("BASE64", Seq(ir.UnresolvedAttribute("a"))) generates "BASE64(a)"
    }

    "BIN(a)" in {
      ir.CallFunction("BIN", Seq(ir.UnresolvedAttribute("a"))) generates "BIN(a)"
    }

    "BIT_AND(a)" in {
      ir.CallFunction("BIT_AND", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_AND(a)"
    }

    "BIT_COUNT(a)" in {
      ir.CallFunction("BIT_COUNT", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_COUNT(a)"
    }

    "BIT_LENGTH(a)" in {
      ir.CallFunction("BIT_LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_LENGTH(a)"
    }

    "BIT_OR(a)" in {
      ir.CallFunction("BIT_OR", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_OR(a)"
    }

    "BIT_XOR(a)" in {
      ir.CallFunction("BIT_XOR", Seq(ir.UnresolvedAttribute("a"))) generates "BIT_XOR(a)"
    }

    "BOOL_AND(a)" in {
      ir.CallFunction("BOOL_AND", Seq(ir.UnresolvedAttribute("a"))) generates "BOOL_AND(a)"
    }

    "BROUND(a, b)" in {
      ir.CallFunction("BROUND", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "BROUND(a, b)"
    }

    "CBRT(a)" in {
      ir.CallFunction("CBRT", Seq(ir.UnresolvedAttribute("a"))) generates "CBRT(a)"
    }

    "CEIL(a)" in {
      ir.CallFunction("CEIL", Seq(ir.UnresolvedAttribute("a"))) generates "CEIL(a)"
    }

    "CHAR(a)" in {
      ir.CallFunction("CHAR", Seq(ir.UnresolvedAttribute("a"))) generates "CHAR(a)"
    }

    "COALESCE(a, b)" in {
      ir.CallFunction(
        "COALESCE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COALESCE(a, b)"
    }

    "ARRAY_AGG(a)" in {
      ir.CollectList(ir.UnresolvedAttribute("a")) generates "ARRAY_AGG(a)"
    }

    "COLLECT_SET(a)" in {
      ir.CallFunction("COLLECT_SET", Seq(ir.UnresolvedAttribute("a"))) generates "COLLECT_SET(a)"
    }

    "CONCAT(a, b)" in {
      ir.CallFunction("CONCAT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CONCAT(a, b)"
    }

    "CONCAT_WS(a, b)" in {
      ir.CallFunction(
        "CONCAT_WS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CONCAT_WS(a, b)"
    }

    "CONV(a, b, c)" in {
      ir.CallFunction(
        "CONV",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "CONV(a, b, c)"
    }

    "CORR(a, b)" in {
      ir.CallFunction("CORR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CORR(a, b)"
    }

    "COS(a)" in {
      ir.CallFunction("COS", Seq(ir.UnresolvedAttribute("a"))) generates "COS(a)"
    }

    "COSH(a)" in {
      ir.CallFunction("COSH", Seq(ir.UnresolvedAttribute("a"))) generates "COSH(a)"
    }

    "COT(a)" in {
      ir.CallFunction("COT", Seq(ir.UnresolvedAttribute("a"))) generates "COT(a)"
    }

    "COUNT(a, b)" in {
      ir.CallFunction("COUNT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COUNT(a, b)"
    }

    "COUNT_IF(a)" in {
      ir.CallFunction("COUNT_IF", Seq(ir.UnresolvedAttribute("a"))) generates "COUNT_IF(a)"
    }

    "COUNT_MIN_SKETCH(a, b, c, d)" in {
      ir.CallFunction(
        "COUNT_MIN_SKETCH",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "COUNT_MIN_SKETCH(a, b, c, d)"
    }

    "COVAR_POP(a, b)" in {
      ir.CallFunction(
        "COVAR_POP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COVAR_POP(a, b)"
    }

    "COVAR_SAMP(a, b)" in {
      ir.CallFunction(
        "COVAR_SAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "COVAR_SAMP(a, b)"
    }

    "CRC32(a)" in {
      ir.CallFunction("CRC32", Seq(ir.UnresolvedAttribute("a"))) generates "CRC32(a)"
    }

    "CUBE(a, b)" in {
      ir.CallFunction("CUBE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "CUBE(a, b)"
    }

    "CUME_DIST()" in {
      ir.CallFunction("CUME_DIST", Seq()) generates "CUME_DIST()"
    }

    "CURRENT_CATALOG()" in {
      ir.CallFunction("CURRENT_CATALOG", Seq()) generates "CURRENT_CATALOG()"
    }

    "CURRENT_DATABASE()" in {
      ir.CallFunction("CURRENT_DATABASE", Seq()) generates "CURRENT_DATABASE()"
    }

    "CURRENT_DATE()" in {
      ir.CallFunction("CURRENT_DATE", Seq()) generates "CURRENT_DATE()"
    }

    "CURRENT_TIMESTAMP()" in {
      ir.CallFunction("CURRENT_TIMESTAMP", Seq()) generates "CURRENT_TIMESTAMP()"
    }

    "CURRENT_TIMEZONE()" in {
      ir.CallFunction("CURRENT_TIMEZONE", Seq()) generates "CURRENT_TIMEZONE()"
    }

    "DATEDIFF(a, b)" in {
      ir.CallFunction(
        "DATEDIFF",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATEDIFF(a, b)"
    }

    "DATE_ADD(a, b)" in {
      ir.CallFunction(
        "DATE_ADD",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_ADD(a, b)"
    }

    "DATE_FORMAT(a, b)" in {
      ir.CallFunction(
        "DATE_FORMAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_FORMAT(a, b)"
    }

    "DATE_FROM_UNIX_DATE(a)" in {
      ir.CallFunction("DATE_FROM_UNIX_DATE", Seq(ir.UnresolvedAttribute("a"))) generates "DATE_FROM_UNIX_DATE(a)"
    }

    "DATE_PART(a, b)" in {
      ir.CallFunction(
        "DATE_PART",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_PART(a, b)"
    }

    "DATE_SUB(a, b)" in {
      ir.CallFunction(
        "DATE_SUB",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_SUB(a, b)"
    }

    "DATE_TRUNC(a, b)" in {
      ir.CallFunction(
        "DATE_TRUNC",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DATE_TRUNC(a, b)"
    }

    "DAYOFMONTH(a)" in {
      ir.CallFunction("DAYOFMONTH", Seq(ir.UnresolvedAttribute("a"))) generates "DAYOFMONTH(a)"
    }

    "DAYOFWEEK(a)" in {
      ir.CallFunction("DAYOFWEEK", Seq(ir.UnresolvedAttribute("a"))) generates "DAYOFWEEK(a)"
    }

    "DAYOFYEAR(a)" in {
      ir.CallFunction("DAYOFYEAR", Seq(ir.UnresolvedAttribute("a"))) generates "DAYOFYEAR(a)"
    }

    "DECODE(a, b)" in {
      ir.CallFunction("DECODE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DECODE(a, b)"
    }

    "DEGREES(a)" in {
      ir.CallFunction("DEGREES", Seq(ir.UnresolvedAttribute("a"))) generates "DEGREES(a)"
    }

    "DENSE_RANK(a, b)" in {
      ir.CallFunction(
        "DENSE_RANK",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DENSE_RANK(a, b)"
    }

    "DIV(a, b)" in {
      ir.CallFunction("DIV", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "DIV(a, b)"
    }

    "E()" in {
      ir.CallFunction("E", Seq()) generates "E()"
    }

    "ELEMENT_AT(a, b)" in {
      ir.CallFunction(
        "ELEMENT_AT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ELEMENT_AT(a, b)"
    }

    "ELT(a, b)" in {
      ir.CallFunction("ELT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ELT(a, b)"
    }

    "ENCODE(a, b)" in {
      ir.CallFunction("ENCODE", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ENCODE(a, b)"
    }

    "EXISTS(a, b)" in {
      ir.CallFunction("EXISTS", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "EXISTS(a, b)"
    }

    "EXP(a)" in {
      ir.CallFunction("EXP", Seq(ir.UnresolvedAttribute("a"))) generates "EXP(a)"
    }

    "EXPLODE(a)" in {
      ir.CallFunction("EXPLODE", Seq(ir.UnresolvedAttribute("a"))) generates "EXPLODE(a)"
    }

    "EXPM1(a)" in {
      ir.CallFunction("EXPM1", Seq(ir.UnresolvedAttribute("a"))) generates "EXPM1(a)"
    }

    "EXTRACT(a FROM b)" in {
      ir.Extract(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "EXTRACT(a FROM b)"
    }
    "FACTORIAL(a)" in {
      ir.CallFunction("FACTORIAL", Seq(ir.UnresolvedAttribute("a"))) generates "FACTORIAL(a)"
    }

    "FILTER(a, b)" in {
      ir.CallFunction("FILTER", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FILTER(a, b)"
    }

    "FIND_IN_SET(a, b)" in {
      ir.CallFunction(
        "FIND_IN_SET",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FIND_IN_SET(a, b)"
    }

    "FIRST(a, b)" in {
      ir.CallFunction("FIRST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FIRST(a, b)"
    }

    "FLATTEN(a)" in {
      ir.CallFunction("FLATTEN", Seq(ir.UnresolvedAttribute("a"))) generates "FLATTEN(a)"
    }

    "FLOOR(a)" in {
      ir.CallFunction("FLOOR", Seq(ir.UnresolvedAttribute("a"))) generates "FLOOR(a)"
    }

    "FORALL(a, b)" in {
      ir.CallFunction("FORALL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FORALL(a, b)"
    }

    "FORMAT_NUMBER(a, b)" in {
      ir.CallFunction(
        "FORMAT_NUMBER",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FORMAT_NUMBER(a, b)"
    }

    "FORMAT_STRING(a, b)" in {
      ir.CallFunction(
        "FORMAT_STRING",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FORMAT_STRING(a, b)"
    }

    "FROM_CSV(a, b, c)" in {
      ir.CallFunction(
        "FROM_CSV",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "FROM_CSV(a, b, c)"
    }

    "FROM_JSON(a, b, c)" in {
      ir.CallFunction(
        "FROM_JSON",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "FROM_JSON(a, b, c)"
    }

    "FROM_UNIXTIME(a, b)" in {
      ir.CallFunction(
        "FROM_UNIXTIME",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FROM_UNIXTIME(a, b)"
    }

    "FROM_UTC_TIMESTAMP(a, b)" in {
      ir.CallFunction(
        "FROM_UTC_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "FROM_UTC_TIMESTAMP(a, b)"
    }

    "GET_JSON_OBJECT(a, b)" in {
      ir.CallFunction(
        "GET_JSON_OBJECT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "GET_JSON_OBJECT(a, b)"
    }

    "GREATEST(a, b)" in {
      ir.CallFunction(
        "GREATEST",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "GREATEST(a, b)"
    }

    "GROUPING(a)" in {
      ir.CallFunction("GROUPING", Seq(ir.UnresolvedAttribute("a"))) generates "GROUPING(a)"
    }

    "GROUPING_ID(a, b)" in {
      ir.CallFunction(
        "GROUPING_ID",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "GROUPING_ID(a, b)"
    }

    "HASH(a, b)" in {
      ir.CallFunction("HASH", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "HASH(a, b)"
    }

    "HEX(a)" in {
      ir.CallFunction("HEX", Seq(ir.UnresolvedAttribute("a"))) generates "HEX(a)"
    }

    "HOUR(a)" in {
      ir.CallFunction("HOUR", Seq(ir.UnresolvedAttribute("a"))) generates "HOUR(a)"
    }

    "HYPOT(a, b)" in {
      ir.CallFunction("HYPOT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "HYPOT(a, b)"
    }

    "IF(a, b, c)" in {
      ir.CallFunction(
        "IF",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "IF(a, b, c)"
    }

    "IFNULL(a, b)" in {
      ir.CallFunction("IFNULL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "IFNULL(a, b)"
    }

    "INITCAP(a)" in {
      ir.CallFunction("INITCAP", Seq(ir.UnresolvedAttribute("a"))) generates "INITCAP(a)"
    }

    "INLINE(a)" in {
      ir.CallFunction("INLINE", Seq(ir.UnresolvedAttribute("a"))) generates "INLINE(a)"
    }

    "INPUT_FILE_BLOCK_LENGTH()" in {
      ir.CallFunction("INPUT_FILE_BLOCK_LENGTH", Seq()) generates "INPUT_FILE_BLOCK_LENGTH()"
    }

    "INPUT_FILE_BLOCK_START()" in {
      ir.CallFunction("INPUT_FILE_BLOCK_START", Seq()) generates "INPUT_FILE_BLOCK_START()"
    }

    "INPUT_FILE_NAME()" in {
      ir.CallFunction("INPUT_FILE_NAME", Seq()) generates "INPUT_FILE_NAME()"
    }

    "INSTR(a, b)" in {
      ir.CallFunction("INSTR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "INSTR(a, b)"
    }

    "ISNAN(a)" in {
      ir.CallFunction("ISNAN", Seq(ir.UnresolvedAttribute("a"))) generates "ISNAN(a)"
    }

    "ISNOTNULL(a)" in {
      ir.CallFunction("ISNOTNULL", Seq(ir.UnresolvedAttribute("a"))) generates "ISNOTNULL(a)"
    }

    "ISNULL(a)" in {
      ir.CallFunction("ISNULL", Seq(ir.UnresolvedAttribute("a"))) generates "ISNULL(a)"
    }

    "JAVA_METHOD(a, b)" in {
      ir.CallFunction(
        "JAVA_METHOD",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "JAVA_METHOD(a, b)"
    }

    "JSON_ARRAY_LENGTH(a)" in {
      ir.CallFunction("JSON_ARRAY_LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "JSON_ARRAY_LENGTH(a)"
    }

    "JSON_OBJECT_KEYS(a)" in {
      ir.CallFunction("JSON_OBJECT_KEYS", Seq(ir.UnresolvedAttribute("a"))) generates "JSON_OBJECT_KEYS(a)"
    }

    "JSON_TUPLE(a, b)" in {
      ir.CallFunction(
        "JSON_TUPLE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "JSON_TUPLE(a, b)"
    }

    "KURTOSIS(a)" in {
      ir.CallFunction("KURTOSIS", Seq(ir.UnresolvedAttribute("a"))) generates "KURTOSIS(a)"
    }

    "LAG(a, b, c)" in {
      ir.CallFunction(
        "LAG",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "LAG(a, b, c)"
    }

    "LAST(a, b)" in {
      ir.CallFunction("LAST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LAST(a, b)"
    }

    "LAST_DAY(a)" in {
      ir.CallFunction("LAST_DAY", Seq(ir.UnresolvedAttribute("a"))) generates "LAST_DAY(a)"
    }

    "LEAD(a, b, c)" in {
      ir.CallFunction(
        "LEAD",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "LEAD(a, b, c)"
    }

    "LEAST(a, b)" in {
      ir.CallFunction("LEAST", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LEAST(a, b)"
    }

    "LEFT(a, b)" in {
      ir.CallFunction("LEFT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LEFT(a, b)"
    }

    "LENGTH(a)" in {
      ir.CallFunction("LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "LENGTH(a)"
    }

    "LEVENSHTEIN(a, b)" in {
      ir.CallFunction(
        "LEVENSHTEIN",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LEVENSHTEIN(a, b)"
    }

    "LN(a)" in {
      ir.CallFunction("LN", Seq(ir.UnresolvedAttribute("a"))) generates "LN(a)"
    }

    "LOG(a, b)" in {
      ir.CallFunction("LOG", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LOG(a, b)"
    }

    "LOG10(a)" in {
      ir.CallFunction("LOG10", Seq(ir.UnresolvedAttribute("a"))) generates "LOG10(a)"
    }

    "LOG1P(a)" in {
      ir.CallFunction("LOG1P", Seq(ir.UnresolvedAttribute("a"))) generates "LOG1P(a)"
    }

    "LOG2(a)" in {
      ir.CallFunction("LOG2", Seq(ir.UnresolvedAttribute("a"))) generates "LOG2(a)"
    }

    "LOWER(a)" in {
      ir.CallFunction("LOWER", Seq(ir.UnresolvedAttribute("a"))) generates "LOWER(a)"
    }

    "LTRIM(a, b)" in {
      ir.CallFunction("LTRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "LTRIM(a, b)"
    }

    "MAKE_DATE(a, b, c)" in {
      ir.CallFunction(
        "MAKE_DATE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "MAKE_DATE(a, b, c)"
    }

    "MAP_CONCAT(a, b)" in {
      ir.CallFunction(
        "MAP_CONCAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAP_CONCAT(a, b)"
    }

    "MAP_ENTRIES(a)" in {
      ir.CallFunction("MAP_ENTRIES", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_ENTRIES(a)"
    }

    "MAP_FILTER(a, b)" in {
      ir.CallFunction(
        "MAP_FILTER",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAP_FILTER(a, b)"
    }

    "MAP_FROM_ARRAYS(a, b)" in {
      ir.CallFunction(
        "MAP_FROM_ARRAYS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAP_FROM_ARRAYS(a, b)"
    }

    "MAP_FROM_ENTRIES(a)" in {
      ir.CallFunction("MAP_FROM_ENTRIES", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_FROM_ENTRIES(a)"
    }

    "MAP_KEYS(a)" in {
      ir.CallFunction("MAP_KEYS", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_KEYS(a)"
    }

    "MAP_VALUES(a)" in {
      ir.CallFunction("MAP_VALUES", Seq(ir.UnresolvedAttribute("a"))) generates "MAP_VALUES(a)"
    }

    "MAP_ZIP_WITH(a, b, c)" in {
      ir.CallFunction(
        "MAP_ZIP_WITH",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "MAP_ZIP_WITH(a, b, c)"
    }

    "MAX(a)" in {
      ir.CallFunction("MAX", Seq(ir.UnresolvedAttribute("a"))) generates "MAX(a)"
    }

    "MAX_BY(a, b)" in {
      ir.CallFunction("MAX_BY", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MAX_BY(a, b)"
    }

    "MD5(a)" in {
      ir.CallFunction("MD5", Seq(ir.UnresolvedAttribute("a"))) generates "MD5(a)"
    }

    "MIN(a)" in {
      ir.CallFunction("MIN", Seq(ir.UnresolvedAttribute("a"))) generates "MIN(a)"
    }

    "MINUTE(a)" in {
      ir.CallFunction("MINUTE", Seq(ir.UnresolvedAttribute("a"))) generates "MINUTE(a)"
    }

    "MIN_BY(a, b)" in {
      ir.CallFunction("MIN_BY", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MIN_BY(a, b)"
    }

    "MOD(a, b)" in {
      ir.CallFunction("MOD", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "MOD(a, b)"
    }

    "MONOTONICALLY_INCREASING_ID()" in {
      ir.CallFunction("MONOTONICALLY_INCREASING_ID", Seq()) generates "MONOTONICALLY_INCREASING_ID()"
    }

    "MONTH(a)" in {
      ir.CallFunction("MONTH", Seq(ir.UnresolvedAttribute("a"))) generates "MONTH(a)"
    }

    "MONTHS_BETWEEN(a, b, c)" in {
      ir.CallFunction(
        "MONTHS_BETWEEN",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "MONTHS_BETWEEN(a, b, c)"
    }

    "NAMED_STRUCT(a, b)" in {
      ir.CallFunction(
        "NAMED_STRUCT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NAMED_STRUCT(a, b)"
    }

    "NANVL(a, b)" in {
      ir.CallFunction("NANVL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NANVL(a, b)"
    }

    "NEGATIVE(a)" in {
      ir.CallFunction("NEGATIVE", Seq(ir.UnresolvedAttribute("a"))) generates "NEGATIVE(a)"
    }

    "NEXT_DAY(a, b)" in {
      ir.CallFunction(
        "NEXT_DAY",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NEXT_DAY(a, b)"
    }

    "NOW()" in {
      ir.CallFunction("NOW", Seq()) generates "NOW()"
    }

    "NTH_VALUE(a, b)" in {
      ir.CallFunction(
        "NTH_VALUE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NTH_VALUE(a, b)"
    }

    "NTILE(a)" in {
      ir.CallFunction("NTILE", Seq(ir.UnresolvedAttribute("a"))) generates "NTILE(a)"
    }

    "NULLIF(a, b)" in {
      ir.CallFunction("NULLIF", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NULLIF(a, b)"
    }

    "NVL(a, b)" in {
      ir.CallFunction("NVL", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "NVL(a, b)"
    }

    "NVL2(a, b, c)" in {
      ir.CallFunction(
        "NVL2",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "NVL2(a, b, c)"
    }
    "OCTET_LENGTH(a)" in {
      ir.CallFunction("OCTET_LENGTH", Seq(ir.UnresolvedAttribute("a"))) generates "OCTET_LENGTH(a)"
    }

    "OR(a, b)" in {
      ir.CallFunction("OR", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "OR(a, b)"
    }

    "OVERLAY(a, b, c, d)" in {
      ir.CallFunction(
        "OVERLAY",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "OVERLAY(a, b, c, d)"
    }

    "PARSE_URL(a, b)" in {
      ir.CallFunction(
        "PARSE_URL",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "PARSE_URL(a, b)"
    }

    "PERCENTILE(a, b, c)" in {
      ir.CallFunction(
        "PERCENTILE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "PERCENTILE(a, b, c)"
    }

    "PERCENTILE_APPROX(a, b, c)" in {
      ir.CallFunction(
        "PERCENTILE_APPROX",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "PERCENTILE_APPROX(a, b, c)"
    }

    "PERCENT_RANK(a, b)" in {
      ir.CallFunction(
        "PERCENT_RANK",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "PERCENT_RANK(a, b)"
    }

    "PI()" in {
      ir.CallFunction("PI", Seq()) generates "PI()"
    }

    "PMOD(a, b)" in {
      ir.CallFunction("PMOD", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "PMOD(a, b)"
    }

    "POSEXPLODE(a)" in {
      ir.CallFunction("POSEXPLODE", Seq(ir.UnresolvedAttribute("a"))) generates "POSEXPLODE(a)"
    }

    "POSITIVE(a)" in {
      ir.CallFunction("POSITIVE", Seq(ir.UnresolvedAttribute("a"))) generates "POSITIVE(a)"
    }

    "POWER(a, b)" in {
      ir.Pow(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "POWER(a, b)"
    }

    "QUARTER(a)" in {
      ir.CallFunction("QUARTER", Seq(ir.UnresolvedAttribute("a"))) generates "QUARTER(a)"
    }

    "RADIANS(a)" in {
      ir.CallFunction("RADIANS", Seq(ir.UnresolvedAttribute("a"))) generates "RADIANS(a)"
    }

    "RAISE_ERROR(a)" in {
      ir.CallFunction("RAISE_ERROR", Seq(ir.UnresolvedAttribute("a"))) generates "RAISE_ERROR(a)"
    }

    "RAND(a)" in {
      ir.CallFunction("RAND", Seq(ir.UnresolvedAttribute("a"))) generates "RAND(a)"
    }

    "RANDN(a)" in {
      ir.CallFunction("RANDN", Seq(ir.UnresolvedAttribute("a"))) generates "RANDN(a)"
    }

    "RANK(a, b)" in {
      ir.CallFunction("RANK", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "RANK(a, b)"
    }

    "REGEXP_EXTRACT(a, b, c)" in {
      ir.CallFunction(
        "REGEXP_EXTRACT",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "REGEXP_EXTRACT(a, b, c)"
    }

    "REGEXP_EXTRACT_ALL(a, b, c)" in {
      ir.CallFunction(
        "REGEXP_EXTRACT_ALL",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "REGEXP_EXTRACT_ALL(a, b, c)"
    }

    "REGEXP_REPLACE(a, b, c, d)" in {
      ir.CallFunction(
        "REGEXP_REPLACE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "REGEXP_REPLACE(a, b, c, d)"
    }

    "REPEAT(a, b)" in {
      ir.CallFunction("REPEAT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "REPEAT(a, b)"
    }

    "REPLACE(a, b, c)" in {
      ir.CallFunction(
        "REPLACE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "REPLACE(a, b, c)"
    }
    "REVERSE(a)" in {
      ir.CallFunction("REVERSE", Seq(ir.UnresolvedAttribute("a"))) generates "REVERSE(a)"
    }

    "RIGHT(a, b)" in {
      ir.CallFunction("RIGHT", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "RIGHT(a, b)"
    }
    "RINT(a)" in {
      ir.CallFunction("RINT", Seq(ir.UnresolvedAttribute("a"))) generates "RINT(a)"
    }

    "a RLIKE b" in {
      ir.RLike(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b")) generates "a RLIKE b"
    }

    "ROLLUP(a, b)" in {
      ir.CallFunction("ROLLUP", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ROLLUP(a, b)"
    }

    "ROUND(a, b)" in {
      ir.CallFunction("ROUND", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "ROUND(a, b)"
    }
    "ROW_NUMBER()" in {
      ir.CallFunction("ROW_NUMBER", Seq()) generates "ROW_NUMBER()"
    }

    "RPAD(a, b, c)" in {
      ir.CallFunction(
        "RPAD",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "RPAD(a, b, c)"
    }

    "RTRIM(a, b)" in {
      ir.CallFunction("RTRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "RTRIM(a, b)"
    }

    "SCHEMA_OF_CSV(a, b)" in {
      ir.CallFunction(
        "SCHEMA_OF_CSV",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SCHEMA_OF_CSV(a, b)"
    }

    "SCHEMA_OF_JSON(a, b)" in {
      ir.CallFunction(
        "SCHEMA_OF_JSON",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SCHEMA_OF_JSON(a, b)"
    }
    "SECOND(a)" in {
      ir.CallFunction("SECOND", Seq(ir.UnresolvedAttribute("a"))) generates "SECOND(a)"
    }

    "SENTENCES(a, b, c)" in {
      ir.CallFunction(
        "SENTENCES",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SENTENCES(a, b, c)"
    }

    "SEQUENCE(a, b, c)" in {
      ir.CallFunction(
        "SEQUENCE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SEQUENCE(a, b, c)"
    }
    "SHA(a)" in {
      ir.CallFunction("SHA", Seq(ir.UnresolvedAttribute("a"))) generates "SHA(a)"
    }

    "SHA2(a, b)" in {
      ir.CallFunction("SHA2", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHA2(a, b)"
    }

    "SHIFTLEFT(a, b)" in {
      ir.CallFunction(
        "SHIFTLEFT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHIFTLEFT(a, b)"
    }

    "SHIFTRIGHT(a, b)" in {
      ir.CallFunction(
        "SHIFTRIGHT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHIFTRIGHT(a, b)"
    }

    "SHIFTRIGHTUNSIGNED(a, b)" in {
      ir.CallFunction(
        "SHIFTRIGHTUNSIGNED",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SHIFTRIGHTUNSIGNED(a, b)"
    }
    "SHUFFLE(a)" in {
      ir.CallFunction("SHUFFLE", Seq(ir.UnresolvedAttribute("a"))) generates "SHUFFLE(a)"
    }
    "SIGN(a)" in {
      ir.CallFunction("SIGN", Seq(ir.UnresolvedAttribute("a"))) generates "SIGN(a)"
    }
    "SIN(a)" in {
      ir.CallFunction("SIN", Seq(ir.UnresolvedAttribute("a"))) generates "SIN(a)"
    }
    "SINH(a)" in {
      ir.CallFunction("SINH", Seq(ir.UnresolvedAttribute("a"))) generates "SINH(a)"
    }
    "SIZE(a)" in {
      ir.CallFunction("SIZE", Seq(ir.UnresolvedAttribute("a"))) generates "SIZE(a)"
    }
    "SKEWNESS(a)" in {
      ir.CallFunction("SKEWNESS", Seq(ir.UnresolvedAttribute("a"))) generates "SKEWNESS(a)"
    }

    "SLICE(a, b, c)" in {
      ir.CallFunction(
        "SLICE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SLICE(a, b, c)"
    }

    "SORT_ARRAY(a, b)" in {
      ir.CallFunction(
        "SORT_ARRAY",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "SORT_ARRAY(a, b)"
    }
    "SOUNDEX(a)" in {
      ir.CallFunction("SOUNDEX", Seq(ir.UnresolvedAttribute("a"))) generates "SOUNDEX(a)"
    }
    "SPACE(a)" in {
      ir.CallFunction("SPACE", Seq(ir.UnresolvedAttribute("a"))) generates "SPACE(a)"
    }
    "SPARK_PARTITION_ID()" in {
      ir.CallFunction("SPARK_PARTITION_ID", Seq()) generates "SPARK_PARTITION_ID()"
    }

    "SPLIT(a, b, c)" in {
      ir.CallFunction(
        "SPLIT",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SPLIT(a, b, c)"
    }

    "SPLIT_PART(a, b, c)" in {
      ir.CallFunction(
        "SPLIT_PART",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SPLIT_PART(a, b, c)"
    }

    "SQRT(a)" in {
      ir.CallFunction("SQRT", Seq(ir.UnresolvedAttribute("a"))) generates "SQRT(a)"
    }

    "STACK(a, b)" in {
      ir.CallFunction("STACK", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "STACK(a, b)"
    }
    "STD(a)" in {
      ir.CallFunction("STD", Seq(ir.UnresolvedAttribute("a"))) generates "STD(a)"
    }
    "STDDEV(a)" in {
      ir.CallFunction("STDDEV", Seq(ir.UnresolvedAttribute("a"))) generates "STDDEV(a)"
    }
    "STDDEV_POP(a)" in {
      ir.CallFunction("STDDEV_POP", Seq(ir.UnresolvedAttribute("a"))) generates "STDDEV_POP(a)"
    }

    "STR_TO_MAP(a, b, c)" in {
      ir.CallFunction(
        "STR_TO_MAP",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "STR_TO_MAP(a, b, c)"
    }

    "SUBSTR(a, b, c)" in {
      ir.CallFunction(
        "SUBSTR",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SUBSTR(a, b, c)"
    }

    "SUBSTRING_INDEX(a, b, c)" in {
      ir.CallFunction(
        "SUBSTRING_INDEX",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "SUBSTRING_INDEX(a, b, c)"
    }
    "SUM(a)" in {
      ir.CallFunction("SUM", Seq(ir.UnresolvedAttribute("a"))) generates "SUM(a)"
    }
    "TAN(a)" in {
      ir.CallFunction("TAN", Seq(ir.UnresolvedAttribute("a"))) generates "TAN(a)"
    }
    "TANH(a)" in {
      ir.CallFunction("TANH", Seq(ir.UnresolvedAttribute("a"))) generates "TANH(a)"
    }
    "TIMESTAMP_MICROS(a)" in {
      ir.CallFunction("TIMESTAMP_MICROS", Seq(ir.UnresolvedAttribute("a"))) generates "TIMESTAMP_MICROS(a)"
    }
    "TIMESTAMP_MILLIS(a)" in {
      ir.CallFunction("TIMESTAMP_MILLIS", Seq(ir.UnresolvedAttribute("a"))) generates "TIMESTAMP_MILLIS(a)"
    }
    "TIMESTAMP_SECONDS(a)" in {
      ir.CallFunction("TIMESTAMP_SECONDS", Seq(ir.UnresolvedAttribute("a"))) generates "TIMESTAMP_SECONDS(a)"
    }

    "TO_CSV(a, b)" in {
      ir.CallFunction("TO_CSV", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_CSV(a, b)"
    }

    "TO_DATE(a, b)" in {
      ir.CallFunction(
        "TO_DATE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_DATE(a, b)"
    }

    "TO_JSON(a, b)" in {
      ir.CallFunction(
        "TO_JSON",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_JSON(a, b)"
    }

    "TO_NUMBER(a, b)" in {
      ir.CallFunction(
        "TO_NUMBER",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_NUMBER(a, b)"
    }

    "TO_TIMESTAMP(a, b)" in {
      ir.CallFunction(
        "TO_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_TIMESTAMP(a, b)"
    }

    "TO_UNIX_TIMESTAMP(a, b)" in {
      ir.CallFunction(
        "TO_UNIX_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_UNIX_TIMESTAMP(a, b)"
    }

    "TO_UTC_TIMESTAMP(a, b)" in {
      ir.CallFunction(
        "TO_UTC_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TO_UTC_TIMESTAMP(a, b)"
    }

    "TRANSFORM(a, b)" in {
      ir.CallFunction(
        "TRANSFORM",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRANSFORM(a, b)"
    }

    "TRANSFORM_KEYS(a, b)" in {
      ir.CallFunction(
        "TRANSFORM_KEYS",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRANSFORM_KEYS(a, b)"
    }

    "TRANSFORM_VALUES(a, b)" in {
      ir.CallFunction(
        "TRANSFORM_VALUES",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRANSFORM_VALUES(a, b)"
    }

    "TRANSLATE(a, b, c)" in {
      ir.CallFunction(
        "TRANSLATE",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "TRANSLATE(a, b, c)"
    }

    "TRIM(a, b)" in {
      ir.CallFunction("TRIM", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRIM(a, b)"
    }

    "TRUNC(a, b)" in {
      ir.CallFunction("TRUNC", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "TRUNC(a, b)"
    }
    "TYPEOF(a)" in {
      ir.CallFunction("TYPEOF", Seq(ir.UnresolvedAttribute("a"))) generates "TYPEOF(a)"
    }
    "UCASE(a)" in {
      ir.CallFunction("UCASE", Seq(ir.UnresolvedAttribute("a"))) generates "UCASE(a)"
    }
    "UNBASE64(a)" in {
      ir.CallFunction("UNBASE64", Seq(ir.UnresolvedAttribute("a"))) generates "UNBASE64(a)"
    }
    "UNHEX(a)" in {
      ir.CallFunction("UNHEX", Seq(ir.UnresolvedAttribute("a"))) generates "UNHEX(a)"
    }
    "UNIX_DATE(a)" in {
      ir.CallFunction("UNIX_DATE", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_DATE(a)"
    }
    "UNIX_MICROS(a)" in {
      ir.CallFunction("UNIX_MICROS", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_MICROS(a)"
    }
    "UNIX_MILLIS(a)" in {
      ir.CallFunction("UNIX_MILLIS", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_MILLIS(a)"
    }
    "UNIX_SECONDS(a)" in {
      ir.CallFunction("UNIX_SECONDS", Seq(ir.UnresolvedAttribute("a"))) generates "UNIX_SECONDS(a)"
    }

    "UNIX_TIMESTAMP(a, b)" in {
      ir.CallFunction(
        "UNIX_TIMESTAMP",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "UNIX_TIMESTAMP(a, b)"
    }
    "UUID()" in {
      ir.CallFunction("UUID", Seq()) generates "UUID()"
    }
    "VAR_POP(a)" in {
      ir.CallFunction("VAR_POP", Seq(ir.UnresolvedAttribute("a"))) generates "VAR_POP(a)"
    }
    "VAR_SAMP(a)" in {
      ir.CallFunction("VAR_SAMP", Seq(ir.UnresolvedAttribute("a"))) generates "VAR_SAMP(a)"
    }
    "VERSION()" in {
      ir.CallFunction("VERSION", Seq()) generates "VERSION()"
    }
    "WEEKDAY(a)" in {
      ir.CallFunction("WEEKDAY", Seq(ir.UnresolvedAttribute("a"))) generates "WEEKDAY(a)"
    }
    "WEEKOFYEAR(a)" in {
      ir.CallFunction("WEEKOFYEAR", Seq(ir.UnresolvedAttribute("a"))) generates "WEEKOFYEAR(a)"
    }

    "WIDTH_BUCKET(a, b, c, d)" in {
      ir.CallFunction(
        "WIDTH_BUCKET",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"),
          ir.UnresolvedAttribute("d"))) generates "WIDTH_BUCKET(a, b, c, d)"
    }

    "XPATH(a, b)" in {
      ir.CallFunction("XPATH", Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH(a, b)"
    }

    "XPATH_BOOLEAN(a, b)" in {
      ir.CallFunction(
        "XPATH_BOOLEAN",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_BOOLEAN(a, b)"
    }

    "XPATH_DOUBLE(a, b)" in {
      ir.CallFunction(
        "XPATH_DOUBLE",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_DOUBLE(a, b)"
    }

    "XPATH_FLOAT(a, b)" in {
      ir.CallFunction(
        "XPATH_FLOAT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_FLOAT(a, b)"
    }

    "XPATH_INT(a, b)" in {
      ir.CallFunction(
        "XPATH_INT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_INT(a, b)"
    }

    "XPATH_LONG(a, b)" in {
      ir.CallFunction(
        "XPATH_LONG",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_LONG(a, b)"
    }

    "XPATH_SHORT(a, b)" in {
      ir.CallFunction(
        "XPATH_SHORT",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_SHORT(a, b)"
    }

    "XPATH_STRING(a, b)" in {
      ir.CallFunction(
        "XPATH_STRING",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XPATH_STRING(a, b)"
    }

    "XXHASH64(a, b)" in {
      ir.CallFunction(
        "XXHASH64",
        Seq(ir.UnresolvedAttribute("a"), ir.UnresolvedAttribute("b"))) generates "XXHASH64(a, b)"
    }
    "YEAR(a)" in {
      ir.CallFunction("YEAR", Seq(ir.UnresolvedAttribute("a"))) generates "YEAR(a)"
    }

    "ZIP_WITH(a, b, c)" in {
      ir.CallFunction(
        "ZIP_WITH",
        Seq(
          ir.UnresolvedAttribute("a"),
          ir.UnresolvedAttribute("b"),
          ir.UnresolvedAttribute("c"))) generates "ZIP_WITH(a, b, c)"
    }
  }

  "literal" should {
    "NULL" in {
      ir.Literal(null) generates "NULL"
    }

    "binary array" in {
      ir.Literal(Array[Byte](0x01, 0x02, 0x03)) generates "010203"
    }

    "booleans" in {
      ir.Literal(true) generates "true"
      ir.Literal(false) generates "false"
    }

    "short" in {
      ir.Literal(123, ir.ShortType) generates "123"
    }

    "123" in {
      ir.Literal(123) generates "123"
    }

    "long" in {
      ir.Literal(123, ir.LongType) generates "123"
    }

    "float" in {
      ir.Literal(123.4f, ir.FloatType) generates "123.4"
    }

    "double" in {
      ir.Literal(123.4, ir.DoubleType) generates "123.4"
    }

    "decimal" in {
      ir.Literal(BigDecimal("123.4")) generates "123.4"
    }

    "string" in {
      ir.Literal("abc") generates "'abc'"
    }

    "string containing single quotes" in {
      ir.Literal("a'b'c") generates "'a\\'b\\'c'"
    }

    "CAST('2024-07-23 18:03:21' AS TIMESTAMP)" in {
      ir.Literal(new Timestamp(1721757801L)) generates "CAST('2024-07-23 18:03:21' AS TIMESTAMP)"
    }

    "CAST('2024-07-23' AS DATE)" in {
      ir.Literal(new Date(1721757801000L)) generates "CAST('2024-07-23' AS DATE)"
    }

    "ARRAY('abc', 'def')" in {
      ir.Literal(Seq("abc", "def")) generates "ARRAY('abc', 'def')"
    }

    "MAP('foo', 'bar', 'baz', 'qux')" in {
      ir.Literal(Map("foo" -> "bar", "baz" -> "qux")) generates "MAP('foo', 'bar', 'baz', 'qux')"
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
          ir.ObjectReference(ir.Id("schema1"), ir.Id("table 1", caseSensitive = true)))) generates "schema1.`table 1`.*"
    }
  }

  "case...when...else" should {
    "be generated" in {
      ir.Case(None, Seq(ir.WhenBranch(ir.Literal(true), ir.Literal(42))), None) generates "CASE WHEN true THEN 42 END"

      ir.Case(
        Some(ir.Id("c1")),
        Seq(ir.WhenBranch(ir.Literal(true), ir.Literal(42))),
        None) generates "CASE c1 WHEN true THEN 42 END"

      ir.Case(
        Some(ir.Id("c1")),
        Seq(ir.WhenBranch(ir.Literal(true), ir.Literal(42))),
        Some(ir.Literal(0))) generates "CASE c1 WHEN true THEN 42 ELSE 0 END"

      ir.Case(
        Some(ir.Id("c1")),
        Seq(ir.WhenBranch(ir.Literal("Answer"), ir.Literal(42)), ir.WhenBranch(ir.Literal("Year"), ir.Literal(2024))),
        Some(ir.Literal(0))) generates "CASE c1 WHEN 'Answer' THEN 42 WHEN 'Year' THEN 2024 ELSE 0 END"

    }
  }

  "IN" should {
    "be generated" in {
      ir.In(
        ir.Id("c1"),
        Seq(
          ir.ScalarSubquery(
            ir.Project(namedTable("table1"), Seq(ir.Id("column1")))))) generates "c1 IN (SELECT column1 FROM table1)"

      ir.In(ir.Id("c1"), Seq(ir.Literal(1), ir.Literal(2), ir.Literal(3))) generates "c1 IN (1, 2, 3)"
    }
  }

  "window functions" should {
    "be generated" in {
      ir.Window(
        ir.RowNumber(),
        Seq(ir.Id("a")),
        Seq(ir.SortOrder(ir.Id("b"), ir.Ascending, ir.NullsFirst)),
        Some(
          ir.WindowFrame(
            ir.RowsFrame,
            ir.CurrentRow,
            ir.NoBoundary))) generates "ROW_NUMBER() OVER (PARTITION BY a ORDER BY b ASC NULLS FIRST ROWS CURRENT ROW)"

      ir.Window(
        ir.RowNumber(),
        Seq(ir.Id("a")),
        Seq(ir.SortOrder(ir.Id("b"), ir.Ascending, ir.NullsFirst)),
        Some(
          ir.WindowFrame(
            ir.RangeFrame,
            ir.CurrentRow,
            ir.FollowingN(
              ir.Literal(42))))) generates "ROW_NUMBER() OVER (PARTITION BY a ORDER BY b ASC NULLS FIRST RANGE BETWEEN CURRENT ROW AND 42 FOLLOWING)"

    }
  }

  "JSON_ACCESS" should {

    "handle valid identifier" in {
      ir.JsonAccess(ir.Id("c1"), ir.Literal("a")) generates "c1['a']"
    }

    "handle invalid identifier" in {
      ir.JsonAccess(ir.Id("c1"), ir.Id("1", caseSensitive = true)) generates "c1[\"1\"]"
    }

    "handle integer literal" in {
      ir.JsonAccess(ir.Id("c1"), ir.Literal(123)) generates "c1[123]"
    }

    "handle string literal" in {
      ir.JsonAccess(ir.Id("c1"), ir.Literal("abc")) generates "c1['abc']"
    }

    "handle dot expression" in {
      ir.JsonAccess(ir.Dot(ir.Id("c1"), ir.Id("c2")), ir.Literal("a")) generates "c1.c2['a']"
    }

    "be generated" in {
      ir.JsonAccess(ir.JsonAccess(ir.Id("c1"), ir.Literal("a")), ir.Literal("b")) generates "c1['a']['b']"

      ir.JsonAccess(
        ir.JsonAccess(
          ir.JsonAccess(ir.Dot(ir.Id("demo"), ir.Id("level_key")), ir.Literal("level_1_key")),
          ir.Literal("level_2_key")),
        ir.Id("1")) generates "demo.level_key['level_1_key']['level_2_key'][\"1\"]"
    }
  }

  "error node in expression tree" should {
    "generate inline error message comment for a and bad text" in {
      ir.And(ir.Id("a"), ir.UnresolvedExpression(ruleText = "bad text", message = "some error message")) generates
        """a AND /* The following issues were detected:
         |
         |   some error message
         |    bad text
         | */""".stripMargin
    }
  }
}
