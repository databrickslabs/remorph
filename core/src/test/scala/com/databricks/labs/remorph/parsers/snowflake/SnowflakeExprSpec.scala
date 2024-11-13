package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeExprSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: SnowflakeExpressionBuilder = vc.expressionBuilder

  private def example(input: String, expectedAst: Expression): Unit = exampleExpr(input, _.expr(), expectedAst)

  private def searchConditionExample(input: String, expectedAst: Expression): Unit =
    exampleExpr(input, _.searchCondition(), expectedAst)

  "SnowflakeExpressionBuilder" should {
    "do something" should {
      val col = Dot(Dot(Dot(Id("d"), Id("s")), Id("t")), Id("column_1"))

      "d.s.sequence_1.NEXTVAL" in {
        example("d.s.sequence_1.NEXTVAL", NextValue("d.s.sequence_1"))
      }
      "d.s.t.column_1[42]" in {
        example(
          "d.s.t.column_1[42]",
          Dot(Dot(Dot(Id("d"), Id("s")), Id("t")), ArrayAccess(Id("column_1"), Literal(42))))
      }
      "d.s.t.column_1:field_1.\"inner field\"" in {
        example(
          "d.s.t.column_1:field_1.\"inner field\"",
          JsonAccess(col, Dot(Id("field_1"), Id("inner field", caseSensitive = true))))
      }
      "d.s.t.column_1 COLLATE 'en_US-trim'" in {
        example("d.s.t.column_1 COLLATE 'en_US-trim'", Collate(col, "en_US-trim"))
      }
    }

    "translate unary arithmetic operators" should {
      "+column_1" in {
        example("+column_1", UPlus(Id("column_1")))
      }
      "+42" in {
        example("+42", UPlus(Literal(42)))
      }
      "-column_1" in {
        example("-column_1", UMinus(Id("column_1")))
      }
      "-42" in {
        example("-42", UMinus(Literal(42)))
      }
      "NOT true" in {
        example("NOT true", Not(Literal.True))
      }
      "NOT column_2" in {
        example("NOT column_2", Not(Id("column_2")))
      }
    }

    "translate binary arithmetic operators" should {
      "1+1" in {
        example("1+1", Add(Literal(1), Literal(1)))
      }
      "2 * column_1" in {
        example("2 * column_1", Multiply(Literal(2), Id("column_1")))
      }
      "column_1 - 1" in {
        example("column_1 - 1", Subtract(Id("column_1"), Literal(1)))
      }
      "column_1/column_2" in {
        example("column_1/column_2", Divide(Id("column_1"), Id("column_2")))
      }
      "42 % 2" in {
        example("42 % 2", Mod(Literal(42), Literal(2)))
      }
      "'foo' || column_1" in {
        example("'foo' || column_1", Concat(Seq(Literal("foo"), Id("column_1"))))
      }
    }

    "translate IFF expression" in {
      example("IFF (true, column_1, column_2)", If(Literal.True, Id("column_1"), Id("column_2")))
    }

    "translate array literals" should {
      "[1, 2, 3]" in {
        example("[1, 2, 3]", ArrayExpr(Seq(Literal(1), Literal(2), Literal(3)), IntegerType))
      }
      "[1, 2, 'three']" in {
        example("[1, 2, 'three']", ArrayExpr(Seq(Literal(1), Literal(2), Literal("three")), IntegerType))
      }
    }

    "translate cast expressions" should {
      "CAST (column_1 AS BOOLEAN)" in {
        example("CAST (column_1 AS BOOLEAN)", Cast(Id("column_1"), BooleanType))
      }
      "TRY_CAST (column_1 AS BOOLEAN)" in {
        example("TRY_CAST (column_1 AS BOOLEAN)", TryCast(Id("column_1"), BooleanType))
      }
      "TO_TIMESTAMP(1234567890)" in {
        example("TO_TIMESTAMP(1234567890)", CallFunction("TO_TIMESTAMP", Seq(Literal(1234567890))))
      }
      "TIME('00:00:00')" in {
        example("TIME('00:00:00')", CallFunction("TO_TIME", Seq(Literal("00:00:00"))))
      }
      "TO_TIME(column_1)" in {
        example("TO_TIME(column_1)", CallFunction("TO_TIME", Seq(Id("column_1"))))
      }
      "DATE(column_1)" in {
        example("DATE(column_1)", CallFunction("TO_DATE", Seq(Id("column_1"))))
      }
      "TO_DATE('2024-05-15')" in {
        example("TO_DATE('2024-05-15')", CallFunction("TO_DATE", Seq(Literal("2024-05-15"))))
      }
      "INTERVAL '1 hour'" in {
        example("INTERVAL '1 hour'", Cast(Literal("1 hour"), IntervalType))
      }
      "42::FLOAT" in {
        example("42::FLOAT", Cast(Literal(42), DoubleType))
      }
      "TO_CHAR(42)" in {
        example("TO_CHAR(42)", CallFunction("TO_VARCHAR", Seq(Literal(42))))
      }
    }

    "translate IN expressions" should {
      "col1 IN (SELECT * FROM t)" in {
        searchConditionExample(
          "col1 IN (SELECT * FROM t)",
          In(Id("col1"), Seq(ScalarSubquery(Project(namedTable("t"), Seq(Star(None)))))))
      }
      "col1 NOT IN (SELECT * FROM t)" in {
        searchConditionExample(
          "col1 NOT IN (SELECT * FROM t)",
          Not(In(Id("col1"), Seq(ScalarSubquery(Project(namedTable("t"), Seq(Star(None))))))))
      }
      "col1 IN (1, 2, 3)" in {
        searchConditionExample("col1 IN (1, 2, 3)", In(Id("col1"), Seq(Literal(1), Literal(2), Literal(3))))
      }
      "col1 NOT IN ('foo', 'bar')" in {
        searchConditionExample("col1 NOT IN ('foo', 'bar')", Not(In(Id("col1"), Seq(Literal("foo"), Literal("bar")))))
      }
    }

    "translate BETWEEN expressions" should {
      "col1 BETWEEN 3.14 AND 42" in {
        searchConditionExample("col1 BETWEEN 3.14 AND 42", Between(Id("col1"), Literal(3.14), Literal(42)))
      }
      "col1 NOT BETWEEN 3.14 AND 42" in {
        searchConditionExample("col1 NOT BETWEEN 3.14 AND 42", Not(Between(Id("col1"), Literal(3.14), Literal(42))))
      }
    }

    "translate LIKE expressions" should {
      "col1 LIKE '%foo'" in {
        searchConditionExample("col1 LIKE '%foo'", Like(Id("col1"), Literal("%foo"), None))
      }
      "col1 ILIKE '%foo'" in {
        searchConditionExample("col1 ILIKE '%foo'", ILike(Id("col1"), Literal("%foo"), None))
      }
      "col1 NOT LIKE '%foo'" in {
        searchConditionExample("col1 NOT LIKE '%foo'", Not(Like(Id("col1"), Literal("%foo"), None)))
      }
      "col1 NOT ILIKE '%foo'" in {
        searchConditionExample("col1 NOT ILIKE '%foo'", Not(ILike(Id("col1"), Literal("%foo"), None)))
      }
      "col1 LIKE '%foo' ESCAPE '^'" in {
        searchConditionExample("col1 LIKE '%foo' ESCAPE '^'", Like(Id("col1"), Literal("%foo"), Some(Literal('^'))))
      }
      "col1 ILIKE '%foo' ESCAPE '^'" in {
        searchConditionExample("col1 ILIKE '%foo' ESCAPE '^'", ILike(Id("col1"), Literal("%foo"), Some(Literal('^'))))
      }
      "col1 NOT LIKE '%foo' ESCAPE '^'" in {
        searchConditionExample(
          "col1 NOT LIKE '%foo' ESCAPE '^'",
          Not(Like(Id("col1"), Literal("%foo"), Some(Literal('^')))))
      }
      "col1 NOT ILIKE '%foo' ESCAPE '^'" in {
        searchConditionExample(
          "col1 NOT ILIKE '%foo' ESCAPE '^'",
          Not(ILike(Id("col1"), Literal("%foo"), Some(Literal('^')))))
      }
      "col1 LIKE ANY ('%foo', 'bar%', '%qux%')" in {
        searchConditionExample(
          "col1 LIKE ANY ('%foo', 'bar%', '%qux%')",
          LikeAny(Id("col1"), Seq(Literal("%foo"), Literal("bar%"), Literal("%qux%"))))
      }
      "col1 LIKE ALL ('%foo', 'bar^%', '%qux%') ESCAPE '^'" in {
        searchConditionExample(
          "col1 LIKE ALL ('%foo', 'bar^%', '%qux%') ESCAPE '^'",
          LikeAll(Id("col1"), Seq(Literal("%foo"), Literal("bar\\^%"), Literal("%qux%"))))
      }
      "col1 ILIKE ANY ('%foo', 'bar^%', '%qux%') ESCAPE '^'" in {
        searchConditionExample(
          "col1 ILIKE ANY ('%foo', 'bar^%', '%qux%') ESCAPE '^'",
          ILikeAny(Id("col1"), Seq(Literal("%foo"), Literal("bar\\^%"), Literal("%qux%"))))
      }
      "col1 ILIKE ALL ('%foo', 'bar%', '%qux%')" in {
        searchConditionExample(
          "col1 ILIKE ALL ('%foo', 'bar%', '%qux%')",
          ILikeAll(Id("col1"), Seq(Literal("%foo"), Literal("bar%"), Literal("%qux%"))))
      }
      "col1 RLIKE '[a-z][A-Z]*'" in {
        searchConditionExample("col1 RLIKE '[a-z][A-Z]*'", RLike(Id("col1"), Literal("[a-z][A-Z]*")))
      }
      "col1 NOT RLIKE '[a-z][A-Z]*'" in {
        searchConditionExample("col1 NOT RLIKE '[a-z][A-Z]*'", Not(RLike(Id("col1"), Literal("[a-z][A-Z]*"))))
      }
    }

    "translate IS [NOT] NULL expressions" should {
      "col1 IS NULL" in {
        searchConditionExample("col1 IS NULL", IsNull(Id("col1")))
      }
      "col1 IS NOT NULL" in {
        searchConditionExample("col1 IS NOT NULL", IsNotNull(Id("col1")))
      }
    }

    "translate DISTINCT expressions" in {
      searchConditionExample("DISTINCT col1", Distinct(Id("col1")))
    }

    "translate WITHIN GROUP expressions" in {
      searchConditionExample(
        "ARRAY_AGG(col1) WITHIN GROUP (ORDER BY col2)",
        WithinGroup(CallFunction("ARRAY_AGG", Seq(Id("col1"))), Seq(SortOrder(Id("col2"), Ascending, NullsLast))))
    }

    "translate JSON path expressions" should {
      "s.f.value:x.y.names[2]" in {
        example(
          "s.f.value:x.y.names[2]",
          JsonAccess(
            Dot(Dot(Id("s"), Id("f")), Id("value")),
            Dot(Dot(Id("x"), Id("y")), ArrayAccess(Id("names"), Literal(2)))))
      }
      "x:inner_obj['nested_field']" in {
        example("x:inner_obj['nested_field']", JsonAccess(Id("x"), JsonAccess(Id("inner_obj"), Id("nested_field"))))
      }
    }

    "translate JSON literals" in {
      example("{'a': 1, 'b': 2}", StructExpr(Seq(Alias(Literal(1), Id("a")), Alias(Literal(2), Id("b")))))
    }
  }
}
