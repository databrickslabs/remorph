package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.Checkpoints.Checkpoint
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeExprSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: SnowflakeExpressionBuilder = new SnowflakeExpressionBuilder

  private def example(input: String, expectedAst: Expression): Unit = exampleExpr(input, _.expr(), expectedAst)

  "SnowflakeExpressionBuilder" should {
    "" in {
      val col = Dot(Dot(Dot(Id("d"), Id("s")), Id("t")), Id("column_1"))

      example("d.s.sequence_1.NEXTVAL", NextValue("d.s.sequence_1"))
      example("d.s.t.column_1[42]", Dot(Dot(Dot(Id("d"), Id("s")), Id("t")), ArrayAccess(Id("column_1"), Literal(42))))
      example(
        "d.s.t.column_1:field_1.\"inner field\"",
        JsonAccess(col, Dot(Id("field_1"), Id("inner field", caseSensitive = true))))
      example("d.s.t.column_1 COLLATE 'en_US-trim'", Collate(col, "en_US-trim"))
    }

    "translate unary arithmetic operators" in {
      example("+column_1", UPlus(Id("column_1")))
      example("+42", UPlus(Literal(42)))
      example("-column_1", UMinus(Id("column_1")))
      example("-42", UMinus(Literal(42)))
      example("NOT true", Not(Literal.True))
      example("NOT column_2", Not(Id("column_2")))
    }

    "translate binary arithmetic operators" in {
      example("1+1", Add(Literal(1), Literal(1)))
      example("2 * column_1", Multiply(Literal(2), Id("column_1")))
      example("column_1 - 1", Subtract(Id("column_1"), Literal(1)))
      example("column_1/column_2", Divide(Id("column_1"), Id("column_2")))
      example("42 % 2", Mod(Literal(42), Literal(2)))
      example("'foo' || column_1", Concat(Seq(Literal("foo"), Id("column_1"))))
    }

    "translate IFF expression" in {
      example("IFF (true, column_1, column_2)", If(Literal.True, Id("column_1"), Id("column_2")))
    }

    "translate array literals" in {
      example("[1, 2, 3]", ArrayExpr(Seq(Literal(1), Literal(2), Literal(3)), IntegerType))

      example("[1, 2, 'three']", ArrayExpr(Seq(Literal(1), Literal(2), Literal("three")), IntegerType))
    }

    "translate cast expressions" should {
      "CAST (column_1 AS BOOLEAN)" in {
        example("CAST (column_1 AS BOOLEAN)", Cast(Id("column_1"), BooleanType))
      }
      "TRY_CAST (column_1 AS BOOLEAN)" in {
        example("TRY_CAST (column_1 AS BOOLEAN)", Cast(Id("column_1"), BooleanType, returnNullOnError = true))
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

    def exprAndPredicateExample(query: String, expectedAst: Expression): Unit = {
      val cp = new Checkpoint()
      cp(exampleExpr(query, _.expr(), expectedAst))
      cp(exampleExpr(query, _.predicate(), expectedAst))
      cp.reportAll()
    }

    "translate IN expressions" should {
      "col1 IN (SELECT * FROM t)" in {
        exprAndPredicateExample(
          "col1 IN (SELECT * FROM t)",
          In(Id("col1"), Seq(ScalarSubquery(Project(namedTable("t"), Seq(Star(None)))))))
      }
      "col1 NOT IN (SELECT * FROM t)" in {
        exprAndPredicateExample(
          "col1 NOT IN (SELECT * FROM t)",
          Not(In(Id("col1"), Seq(ScalarSubquery(Project(namedTable("t"), Seq(Star(None))))))))
      }
      "col1 IN (1, 2, 3)" in {
        exprAndPredicateExample("col1 IN (1, 2, 3)", In(Id("col1"), Seq(Literal(1), Literal(2), Literal(3))))
      }
      "col1 NOT IN ('foo', 'bar')" in {
        exprAndPredicateExample("col1 NOT IN ('foo', 'bar')", Not(In(Id("col1"), Seq(Literal("foo"), Literal("bar")))))
      }
    }

    "translate BETWEEN expressions" should {
      "col1 BETWEEN 3.14 AND 42" in {
        exprAndPredicateExample(
          "col1 BETWEEN 3.14 AND 42",
          And(GreaterThanOrEqual(Id("col1"), Literal(3.14)), LessThanOrEqual(Id("col1"), Literal(42))))
      }
      "col1 NOT BETWEEN 3.14 AND 42" in {
        exprAndPredicateExample(
          "col1 NOT BETWEEN 3.14 AND 42",
          Not(And(GreaterThanOrEqual(Id("col1"), Literal(3.14)), LessThanOrEqual(Id("col1"), Literal(42)))))
      }
    }

    "translate LIKE expressions" should {
      "col1 LIKE '%foo'" in {
        exprAndPredicateExample("col1 LIKE '%foo'", Like(Id("col1"), Literal("%foo")))
      }
      "col1 ILIKE '%foo'" in {
        exprAndPredicateExample("col1 ILIKE '%foo'", ILike(Id("col1"), Literal("%foo")))
      }
      "col1 NOT LIKE '%foo'" in {
        exprAndPredicateExample("col1 NOT LIKE '%foo'", Not(Like(Id("col1"), Literal("%foo"))))
      }
      "col1 NOT ILIKE '%foo'" in {
        exprAndPredicateExample("col1 NOT ILIKE '%foo'", Not(ILike(Id("col1"), Literal("%foo"))))
      }
      "col1 LIKE '%foo' ESCAPE '^'" in {
        exprAndPredicateExample("col1 LIKE '%foo' ESCAPE '^'", Like(Id("col1"), Literal("%foo"), '^'))
      }
      "col1 ILIKE '%foo' ESCAPE '^'" in {
        exprAndPredicateExample("col1 ILIKE '%foo' ESCAPE '^'", ILike(Id("col1"), Literal("%foo"), '^'))
      }
      "col1 NOT LIKE '%foo' ESCAPE '^'" in {
        exprAndPredicateExample("col1 NOT LIKE '%foo' ESCAPE '^'", Not(Like(Id("col1"), Literal("%foo"), '^')))
      }
      "col1 NOT ILIKE '%foo' ESCAPE '^'" in {
        exprAndPredicateExample("col1 NOT ILIKE '%foo' ESCAPE '^'", Not(ILike(Id("col1"), Literal("%foo"), '^')))
      }
      "col1 LIKE ANY ('%foo', 'bar%', '%qux%')" in {
        exprAndPredicateExample(
          "col1 LIKE ANY ('%foo', 'bar%', '%qux%')",
          LikeAny(Id("col1"), Seq(Literal("%foo"), Literal("bar%"), Literal("%qux%"))))
      }
      "col1 LIKE ALL ('%foo', 'bar^%', '%qux%') ESCAPE '^'" in {
        exprAndPredicateExample(
          "col1 LIKE ALL ('%foo', 'bar^%', '%qux%') ESCAPE '^'",
          LikeAll(Id("col1"), Seq(Literal("%foo"), Literal("bar\\^%"), Literal("%qux%"))))
      }
      "col1 ILIKE ANY ('%foo', 'bar^%', '%qux%') ESCAPE '^'" in {
        exprAndPredicateExample(
          "col1 ILIKE ANY ('%foo', 'bar^%', '%qux%') ESCAPE '^'",
          ILikeAny(Id("col1"), Seq(Literal("%foo"), Literal("bar\\^%"), Literal("%qux%"))))
      }
      "col1 ILIKE ALL ('%foo', 'bar%', '%qux%')" in {
        exprAndPredicateExample(
          "col1 ILIKE ALL ('%foo', 'bar%', '%qux%')",
          ILikeAll(Id("col1"), Seq(Literal("%foo"), Literal("bar%"), Literal("%qux%"))))
      }
      "col1 RLIKE '[a-z][A-Z]*'" in {
        exprAndPredicateExample("col1 RLIKE '[a-z][A-Z]*'", RLike(Id("col1"), Literal("[a-z][A-Z]*")))
      }
      "col1 NOT RLIKE '[a-z][A-Z]*'" in {
        exprAndPredicateExample("col1 NOT RLIKE '[a-z][A-Z]*'", Not(RLike(Id("col1"), Literal("[a-z][A-Z]*"))))
      }
    }

    "translate IS [NOT] NULL expressions" in {
      exprAndPredicateExample("col1 IS NULL", IsNull(Id("col1")))
      exprAndPredicateExample("col1 IS NOT NULL", IsNotNull(Id("col1")))
    }

    "translate DISTINCT expressions" in {
      exprAndPredicateExample("DISTINCT col1", Distinct(Id("col1")))
    }

    "translate WITHIN GROUP expressions" in {
      exprAndPredicateExample(
        "ARRAY_AGG(col1) WITHIN GROUP (ORDER BY col2)",
        WithinGroup(CallFunction("ARRAY_AGG", Seq(Id("col1"))), Seq(SortOrder(Id("col2"), Ascending, NullsLast))))
    }

    "translate JSON path expressions" in {
      example(
        "s.f.value:x.y.names[2]",
        JsonAccess(
          Dot(Dot(Id("s"), Id("f")), Id("value")),
          Dot(Dot(Id("x"), Id("y")), ArrayAccess(Id("names"), Literal(2)))))

      example("x:inner_obj['nested_field']", JsonAccess(Id("x"), JsonAccess(Id("inner_obj"), Id("nested_field"))))
    }

    "translate JSON literals" in {
      example("{'a': 1, 'b': 2}", JsonExpr(UnresolvedType, Seq("a" -> Literal(1), "b" -> Literal(2))))
    }
  }
}
