package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake
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
      example(
        "d.s.t.column_1[42]",
        Dot(Dot(Dot(Id("d"), Id("s")), Id("t")), ArrayAccess(Id("column_1"), Literal(short = Some(42)))))
      example(
        "d.s.t.column_1:field_1.\"inner field\"",
        JsonAccess(col, Dot(Id("field_1"), Id("inner field", caseSensitive = true))))
      example("d.s.t.column_1 COLLATE 'en_US-trim'", Collate(col, "en_US-trim"))
    }

    "translate unary arithmetic operators" in {
      example("+column_1", UPlus(Id("column_1")))
      example("+42", UPlus(Literal(short = Some(42))))
      example("-column_1", UMinus(Id("column_1")))
      example("-42", UMinus(Literal(short = Some(42))))
      example("NOT true", Not(Literal(boolean = Some(true))))
      example("NOT column_2", Not(Id("column_2")))
    }

    "translate binary arithmetic operators" in {
      example("1+1", Add(Literal(short = Some(1)), Literal(short = Some(1))))
      example("2 * column_1", Multiply(Literal(short = Some(2)), Id("column_1")))
      example("column_1 - 1", Subtract(Id("column_1"), Literal(short = Some(1))))
      example("column_1/column_2", Divide(Id("column_1"), Id("column_2")))
      example("42 % 2", Mod(Literal(short = Some(42)), Literal(short = Some(2))))
      example("'foo' || column_1", Concat(Seq(Literal(string = Some("foo")), Id("column_1"))))
    }

    "translate IFF expression" in {
      example("IFF (true, column_1, column_2)", Iff(Literal(boolean = Some(true)), Id("column_1"), Id("column_2")))
    }

    "translate array literals" in {
      example(
        "[1, 2, 3]",
        Literal(array = Some(
          ArrayExpr(
            UnresolvedType,
            Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(short = Some(3)))))))

      example(
        "[1, 2, 'three']",
        Literal(array = Some(
          ArrayExpr(
            UnresolvedType,
            Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(string = Some("three")))))))
    }

    "translate cast expressions" in {
      example("CAST (column_1 AS BOOLEAN)", Cast(Id("column_1"), BooleanType))
      example("TRY_CAST (column_1 AS BOOLEAN)", Cast(Id("column_1"), BooleanType, returnNullOnError = true))
      example("TO_TIMESTAMP(1234567890)", CallFunction("TO_TIMESTAMP", Seq(Literal(integer = Some(1234567890)))))
      example("TIME('00:00:00')", CallFunction("TO_TIME", Seq(Literal(string = Some("00:00:00")))))
      example("TO_TIME(column_1)", CallFunction("TO_TIME", Seq(Id("column_1"))))
      example("DATE(column_1)", CallFunction("TO_DATE", Seq(Id("column_1"))))
      example("TO_DATE('2024-05-15')", CallFunction("TO_DATE", Seq(Literal(string = Some("2024-05-15")))))
      example("INTERVAL '1 hour'", Cast(Literal(string = Some("1 hour")), IntervalType))
      example("42::FLOAT", Cast(Literal(short = Some(42)), DoubleType))
      example("TO_CHAR(42)", CallFunction("TO_VARCHAR", Seq(Literal(short = Some(42)))))
    }

    def exprAndPredicateExample(query: String, expectedAst: Expression): Unit = {
      val cp = new Checkpoint()
      cp(exampleExpr(query, _.expr(), expectedAst))
      cp(exampleExpr(query, _.predicate(), expectedAst))
      cp.reportAll()
    }

    "translate IN expressions" in {
      exprAndPredicateExample(
        "col1 IN (SELECT * FROM t)",
        snowflake.IsInRelation(Project(namedTable("t"), Seq(Star(None))), Id("col1")))
      exprAndPredicateExample(
        "col1 NOT IN (SELECT * FROM t)",
        Not(snowflake.IsInRelation(Project(namedTable("t"), Seq(Star(None))), Id("col1"))))

      exprAndPredicateExample(
        "col1 IN (1, 2, 3)",
        snowflake.IsInCollection(
          Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(short = Some(3))),
          Id("col1")))
      exprAndPredicateExample(
        "col1 NOT IN ('foo', 'bar')",
        Not(snowflake.IsInCollection(Seq(Literal(string = Some("foo")), Literal(string = Some("bar"))), Id("col1"))))

    }

    "translate BETWEEN expressions" in {
      exprAndPredicateExample(
        "col1 BETWEEN 3.14 AND 42",
        And(
          GreaterThanOrEqual(Id("col1"), Literal(float = Some(3.14f))),
          LessThanOrEqual(Id("col1"), Literal(short = Some(42)))))
      exprAndPredicateExample(
        "col1 NOT BETWEEN 3.14 AND 42",
        Not(
          And(
            GreaterThanOrEqual(Id("col1"), Literal(float = Some(3.14f))),
            LessThanOrEqual(Id("col1"), Literal(short = Some(42))))))
    }

    "translate LIKE expressions" in {
      exprAndPredicateExample(
        "col1 LIKE '%foo'",
        snowflake.LikeSnowflake(Id("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = true))
      exprAndPredicateExample(
        "col1 ILIKE '%foo'",
        snowflake.LikeSnowflake(Id("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = false))
      exprAndPredicateExample(
        "col1 NOT LIKE '%foo'",
        Not(snowflake.LikeSnowflake(Id("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = true)))
      exprAndPredicateExample(
        "col1 NOT ILIKE '%foo'",
        Not(snowflake.LikeSnowflake(Id("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = false)))
      exprAndPredicateExample(
        "col1 LIKE '%foo' ESCAPE '^'",
        snowflake.LikeSnowflake(
          Id("col1"),
          Seq(Literal(string = Some("%foo"))),
          Some(Literal(string = Some("^"))),
          caseSensitive = true))
      exprAndPredicateExample(
        "col1 ILIKE '%foo' ESCAPE '^'",
        snowflake.LikeSnowflake(
          Id("col1"),
          Seq(Literal(string = Some("%foo"))),
          Some(Literal(string = Some("^"))),
          caseSensitive = false))

      exprAndPredicateExample(
        "col1 NOT LIKE '%foo' ESCAPE '^'",
        Not(
          snowflake.LikeSnowflake(
            Id("col1"),
            Seq(Literal(string = Some("%foo"))),
            Some(Literal(string = Some("^"))),
            caseSensitive = true)))
      exprAndPredicateExample(
        "col1 NOT ILIKE '%foo' ESCAPE '^'",
        Not(
          snowflake.LikeSnowflake(
            Id("col1"),
            Seq(Literal(string = Some("%foo"))),
            Some(Literal(string = Some("^"))),
            caseSensitive = false)))

      exprAndPredicateExample(
        "col1 LIKE ANY ('%foo', 'bar%', '%qux%')",
        snowflake.LikeSnowflake(
          Id("col1"),
          Seq(Literal(string = Some("%foo")), Literal(string = Some("bar%")), Literal(string = Some("%qux%"))),
          None,
          caseSensitive = true))

      exprAndPredicateExample(
        "col1 LIKE ANY ('%foo', 'bar%', '%qux%') ESCAPE '^'",
        snowflake.LikeSnowflake(
          Id("col1"),
          Seq(Literal(string = Some("%foo")), Literal(string = Some("bar%")), Literal(string = Some("%qux%"))),
          Some(Literal(string = Some("^"))),
          caseSensitive = true))

      exprAndPredicateExample("col1 RLIKE '[a-z][A-Z]*'", RLike(Id("col1"), Literal(string = Some("[a-z][A-Z]*"))))
      exprAndPredicateExample(
        "col1 NOT RLIKE '[a-z][A-Z]*'",
        Not(RLike(Id("col1"), Literal(string = Some("[a-z][A-Z]*")))))
    }

    "translate IS [NOT] NULL expressions" in {
      exprAndPredicateExample("col1 IS NULL", IsNull(Id("col1")))
      exprAndPredicateExample("col1 IS NOT NULL", Not(IsNull(Id("col1"))))
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
          Dot(Dot(Id("x"), Id("y")), ArrayAccess(Id("names"), Literal(short = Some(2))))))

      example("x:inner_obj['nested_field']", JsonAccess(Id("x"), JsonAccess(Id("inner_obj"), Id("nested_field"))))
    }

    "translate JSON literals" in {
      example(
        "{'a': 1, 'b': 2}",
        Literal(json =
          Some(JsonExpr(UnresolvedType, Seq("a" -> Literal(short = Some(1)), "b" -> Literal(short = Some(2)))))))
    }

  }

}
