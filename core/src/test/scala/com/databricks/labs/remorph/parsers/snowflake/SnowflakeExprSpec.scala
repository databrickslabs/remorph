package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.IRHelpers
import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.Assertion
import org.scalatest.Checkpoints.Checkpoint
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeExprSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: SnowflakeExpressionBuilder = new SnowflakeExpressionBuilder

  private def example(input: String, expectedAst: Expression): Assertion = example(input, _.expr(), expectedAst)

  "SnowflakeExpressionBuilder" should {
    "" in {
      val col = Column(Some(ObjectReference(Id("d"), Id("s"), Id("t"))), Id("column_1"))

      example("d.s.sequence_1.NEXTVAL", NextValue("d.s.sequence_1"))
      example("d.s.t.column_1[41 + 1]", ArrayAccess(col, Add(Literal(short = Some(41)), Literal(short = Some(1)))))
      example("d.s.t.column_1:field_1.\"inner field\"", JsonAccess(col, Seq("field_1", "inner field")))
      example("d.s.t.column_1 COLLATE 'en_US-trim'", Collate(col, "en_US-trim"))
    }

    "translate unary arithmetic operators" in {
      example("+column_1", UPlus(simplyNamedColumn("column_1")))
      example("+42", UPlus(Literal(short = Some(42))))
      example("-column_1", UMinus(simplyNamedColumn("column_1")))
      example("-42", UMinus(Literal(short = Some(42))))
      example("NOT true", Not(Literal(boolean = Some(true))))
      example("NOT column_2", Not(simplyNamedColumn("column_2")))
    }

    "translate binary arithmetic operators" in {
      example("1+1", Add(Literal(short = Some(1)), Literal(short = Some(1))))
      example("2 * column_1", Multiply(Literal(short = Some(2)), simplyNamedColumn("column_1")))
      example("column_1 - 1", Subtract(simplyNamedColumn("column_1"), Literal(short = Some(1))))
      example("column_1/column_2", Divide(simplyNamedColumn("column_1"), simplyNamedColumn("column_2")))
      example("42 % 2", Mod(Literal(short = Some(42)), Literal(short = Some(2))))
      example("'foo' || column_1", Concat(Literal(string = Some("foo")), simplyNamedColumn("column_1")))
    }

    "translate IFF expression" in {
      example(
        "IFF (true, column_1, column_2)",
        Iff(Literal(boolean = Some(true)), simplyNamedColumn("column_1"), simplyNamedColumn("column_2")))
    }

    "translate array literals" in {
      example(
        "[1, 2, 3]",
        Literal(array =
          Some(ArrayExpr(None, Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(short = Some(3)))))))
      example("[1,column_1,2]", UnresolvedExpression("[1,column_1,2]"))
    }

    "translate cast expressions" in {
      example("CAST (column_1 AS BOOLEAN)", Cast(simplyNamedColumn("column_1"), BooleanType()))
      example(
        "TRY_CAST (column_1 AS BOOLEAN)",
        Cast(simplyNamedColumn("column_1"), BooleanType(), returnNullOnError = true))
      example("TO_TIMESTAMP(1234567890)", CallFunction("TO_TIMESTAMP", Seq(Literal(integer = Some(1234567890)))))
      example("TIME('00:00:00')", CallFunction("TO_TIME", Seq(Literal(string = Some("00:00:00")))))
      example("TO_TIME(column_1)", CallFunction("TO_TIME", Seq(simplyNamedColumn("column_1"))))
      example("DATE(column_1)", CallFunction("TO_DATE", Seq(simplyNamedColumn("column_1"))))
      example("TO_DATE('2024-05-15')", CallFunction("TO_DATE", Seq(Literal(string = Some("2024-05-15")))))
      example("INTERVAL '1 hour'", Cast(Literal(string = Some("1 hour")), IntervalType()))
      example("42::FLOAT", Cast(Literal(short = Some(42)), DoubleType()))
      example("TO_CHAR(42)", CallFunction("TO_VARCHAR", Seq(Literal(short = Some(42)))))
    }

    def exprAndPredicateExample(query: String, expectedAst: Expression): Unit = {
      val cp = new Checkpoint()
      cp(example(query, _.expr(), expectedAst))
      cp(example(query, _.predicate(), expectedAst))
      cp.reportAll()
    }

    "translate IN expressions" in {
      exprAndPredicateExample(
        "col1 IN (SELECT * FROM t)",
        IsIn(Project(namedTable("t"), Seq(Star(None))), simplyNamedColumn("col1")))
      exprAndPredicateExample(
        "col1 NOT IN (SELECT * FROM t)",
        Not(IsIn(Project(namedTable("t"), Seq(Star(None))), simplyNamedColumn("col1"))))
    }

    "translate BETWEEN expressions" in {
      exprAndPredicateExample(
        "col1 BETWEEN 3.14 AND 42",
        And(
          GreaterThanOrEqual(simplyNamedColumn("col1"), Literal(float = Some(3.14f))),
          LesserThanOrEqual(simplyNamedColumn("col1"), Literal(short = Some(42)))))
      exprAndPredicateExample(
        "col1 NOT BETWEEN 3.14 AND 42",
        Not(
          And(
            GreaterThanOrEqual(simplyNamedColumn("col1"), Literal(float = Some(3.14f))),
            LesserThanOrEqual(simplyNamedColumn("col1"), Literal(short = Some(42))))))
    }

    "translate LIKE expressions" in {
      exprAndPredicateExample(
        "col1 LIKE '%foo'",
        Like(simplyNamedColumn("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = true))
      exprAndPredicateExample(
        "col1 ILIKE '%foo'",
        Like(simplyNamedColumn("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = false))
      exprAndPredicateExample(
        "col1 NOT LIKE '%foo'",
        Not(Like(simplyNamedColumn("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = true)))
      exprAndPredicateExample(
        "col1 NOT ILIKE '%foo'",
        Not(Like(simplyNamedColumn("col1"), Seq(Literal(string = Some("%foo"))), None, caseSensitive = false)))
      exprAndPredicateExample(
        "col1 LIKE '%foo' ESCAPE '^'",
        Like(
          simplyNamedColumn("col1"),
          Seq(Literal(string = Some("%foo"))),
          Some(Literal(string = Some("^"))),
          caseSensitive = true))
      exprAndPredicateExample(
        "col1 ILIKE '%foo' ESCAPE '^'",
        Like(
          simplyNamedColumn("col1"),
          Seq(Literal(string = Some("%foo"))),
          Some(Literal(string = Some("^"))),
          caseSensitive = false))

      exprAndPredicateExample(
        "col1 NOT LIKE '%foo' ESCAPE '^'",
        Not(
          Like(
            simplyNamedColumn("col1"),
            Seq(Literal(string = Some("%foo"))),
            Some(Literal(string = Some("^"))),
            caseSensitive = true)))
      exprAndPredicateExample(
        "col1 NOT ILIKE '%foo' ESCAPE '^'",
        Not(
          Like(
            simplyNamedColumn("col1"),
            Seq(Literal(string = Some("%foo"))),
            Some(Literal(string = Some("^"))),
            caseSensitive = false)))

      exprAndPredicateExample(
        "col1 LIKE ANY ('%foo', 'bar%', '%qux%')",
        Like(
          simplyNamedColumn("col1"),
          Seq(Literal(string = Some("%foo")), Literal(string = Some("bar%")), Literal(string = Some("%qux%"))),
          None,
          caseSensitive = true))

      exprAndPredicateExample(
        "col1 LIKE ANY ('%foo', 'bar%', '%qux%') ESCAPE '^'",
        Like(
          simplyNamedColumn("col1"),
          Seq(Literal(string = Some("%foo")), Literal(string = Some("bar%")), Literal(string = Some("%qux%"))),
          Some(Literal(string = Some("^"))),
          caseSensitive = true))

      exprAndPredicateExample(
        "col1 RLIKE '[a-z][A-Z]*'",
        RLike(simplyNamedColumn("col1"), Literal(string = Some("[a-z][A-Z]*"))))
      exprAndPredicateExample(
        "col1 NOT RLIKE '[a-z][A-Z]*'",
        Not(RLike(simplyNamedColumn("col1"), Literal(string = Some("[a-z][A-Z]*")))))
    }

    "translate IS [NOT] NULL expressions" in {
      exprAndPredicateExample("col1 IS NULL", IsNull(simplyNamedColumn("col1")))
      exprAndPredicateExample("col1 IS NOT NULL", Not(IsNull(simplyNamedColumn("col1"))))
    }

    "translate DISTINCT expressions" in {
      exprAndPredicateExample("DISTINCT col1", Distinct(simplyNamedColumn("col1")))
    }

    "translate WITHIN GROUP expressions" in {
      exprAndPredicateExample(
        "ARRAY_AGG(col1) WITHIN GROUP (ORDER BY col2)",
        WithinGroup(
          CallFunction("ARRAY_AGG", Seq(simplyNamedColumn("col1"))),
          Seq(SortOrder(simplyNamedColumn("col2"), AscendingSortDirection, SortNullsLast))))
    }
  }

}
