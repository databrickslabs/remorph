package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{ComparisonOperatorContext, LiteralContext}
import org.mockito.Mockito._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeExpressionBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: SnowflakeExpressionBuilder =
    new SnowflakeExpressionBuilder

  "SnowflakeExpressionBuilder" should {
    "translate literals" in {
      exampleExpr("null", _.literal(), Literal(nullType = Some(NullType)))
      exampleExpr("true", _.literal(), Literal(boolean = Some(true)))
      exampleExpr("false", _.literal(), Literal(boolean = Some(false)))
      exampleExpr("1", _.literal(), Literal(short = Some(1)))
      exampleExpr(Int.MaxValue.toString, _.literal(), Literal(integer = Some(Int.MaxValue)))
      exampleExpr("-1", _.literal(), Literal(short = Some(-1)))
      exampleExpr("1.1", _.literal(), Literal(float = Some(1.1f)))
      exampleExpr("1.1e2", _.literal(), Literal(short = Some(110)))
      exampleExpr(Long.MaxValue.toString, _.literal(), Literal(long = Some(Long.MaxValue)))
      exampleExpr("1.1e-2", _.literal(), Literal(float = Some(0.011f)))
      exampleExpr("0.123456789", _.literal(), Literal(double = Some(0.123456789)))
      exampleExpr("0.123456789e-1234", _.literal(), Literal(decimal = Some(Decimal("0.123456789e-1234", None, None))))
      exampleExpr("'foo'", _.literal(), Literal(string = Some("foo")))
      exampleExpr("DATE'1970-01-01'", _.literal(), Literal(date = Some(0)))
      exampleExpr("TIMESTAMP'1970-01-01 00:00:00'", _.literal(), Literal(timestamp = Some(0)))
    }

    "translate ids (quoted or not)" in {
      exampleExpr("foo", _.id(), Id("foo"))
      exampleExpr("\"foo\"", _.id(), Id("foo", caseSensitive = true))
      exampleExpr("\"foo \"\"quoted bar\"\"\"", _.id(), Id("foo \"quoted bar\"", caseSensitive = true))
    }

    "translate column names" in {
      exampleExpr("x", _.columnName(), simplyNamedColumn("x"))
      exampleExpr(
        "\"My Table\".x",
        _.columnName(),
        Column(Some(ObjectReference(Id("My Table", caseSensitive = true))), Id("x")))
    }

    "translate functions with special syntax" in {

      exampleExpr("EXTRACT(day FROM date1)", _.builtinFunction(), CallFunction("EXTRACT", Seq(Id("day"), Id("date1"))))

      exampleExpr(
        "EXTRACT('day' FROM date1)",
        _.builtinFunction(),
        CallFunction("EXTRACT", Seq(Id("day"), Id("date1"))))
    }

    "translate functions named with a keyword" in {
      exampleExpr("LEFT(foo, bar)", _.standardFunction(), CallFunction("LEFT", Seq(Id("foo"), Id("bar"))))
      exampleExpr("RIGHT(foo, bar)", _.standardFunction(), CallFunction("RIGHT", Seq(Id("foo"), Id("bar"))))
    }
    "translate aggregation functions" in {
      exampleExpr("COUNT(x)", _.aggregateFunction(), CallFunction("COUNT", Seq(Id("x"))))
      exampleExpr("AVG(x)", _.aggregateFunction(), CallFunction("AVG", Seq(Id("x"))))
      exampleExpr("SUM(x)", _.aggregateFunction(), CallFunction("SUM", Seq(Id("x"))))
      exampleExpr("MIN(x)", _.aggregateFunction(), CallFunction("MIN", Seq(Id("x"))))

      exampleExpr("COUNT(*)", _.aggregateFunction(), CallFunction("COUNT", Seq(Star(None))))

      exampleExpr(
        "LISTAGG(x, ',')",
        _.aggregateFunction(),
        CallFunction("LISTAGG", Seq(Id("x"), Literal(string = Some(",")))))
      exampleExpr("ARRAY_AGG(x)", _.aggregateFunction(), CallFunction("ARRAYAGG", Seq(Id("x"))))
    }

    "translate a query with a window function" in {

      exampleExpr(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("ROW_NUMBER", Seq()),
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(Id("a"), Descending, NullsFirst)),
          frame_spec = None))

      exampleExpr(
        query = "ROW_NUMBER() OVER (PARTITION BY a)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("ROW_NUMBER", Seq()),
          partition_spec = Seq(Id("a")),
          sort_order = Seq(),
          frame_spec = None))
      exampleExpr(
        query = "NTILE(42) OVER (PARTITION BY a ORDER BY b, c DESC, d)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("NTILE", Seq(Literal(short = Some(42)))),
          partition_spec = Seq(Id("a")),
          sort_order = Seq(
            SortOrder(Id("b"), Ascending, NullsLast),
            SortOrder(Id("c"), Descending, NullsFirst),
            SortOrder(Id("d"), Ascending, NullsLast)),
          frame_spec = None))
    }

    "translate window frame specifications" in {

      exampleExpr(
        query = "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("ROW_NUMBER", Seq()),
          partition_spec = Seq(Id("a")),
          sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
          frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, CurrentRow))))

      exampleExpr(
        query = "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("ROW_NUMBER", Seq()),
          partition_spec = Seq(Id("a")),
          sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
          frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, UnboundedFollowing))))

      exampleExpr(
        query = "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN 42 PRECEDING AND CURRENT ROW)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("ROW_NUMBER", Seq()),
          partition_spec = Seq(Id("a")),
          sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
          frame_spec = Some(WindowFrame(RowsFrame, PrecedingN(Literal(short = Some(42))), CurrentRow))))

      exampleExpr(
        query = "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN CURRENT ROW AND 42 FOLLOWING)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = CallFunction("ROW_NUMBER", Seq()),
          partition_spec = Seq(Id("a")),
          sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
          frame_spec = Some(WindowFrame(RowsFrame, CurrentRow, FollowingN(Literal(short = Some(42)))))))
    }

    "translate star-expressions" in {
      exampleExpr("*", _.columnElemStar(), Star(None))
      exampleExpr("t.*", _.columnElemStar(), Star(Some(ObjectReference(Id("t")))))
      exampleExpr(
        "db1.schema1.table1.*",
        _.columnElemStar(),
        Star(Some(ObjectReference(Id("db1"), Id("schema1"), Id("table1")))))
    }
  }

  "SnowflakeExpressionBuilder.buildSortOrder" should {

    "translate ORDER BY a" in {
      val tree = parseString("ORDER BY a", _.orderByClause())
      astBuilder.buildSortOrder(tree) shouldBe Seq(SortOrder(Id("a"), Ascending, NullsLast))
    }

    "translate ORDER BY a ASC NULLS FIRST" in {
      val tree = parseString("ORDER BY a ASC NULLS FIRST", _.orderByClause())
      astBuilder.buildSortOrder(tree) shouldBe Seq(SortOrder(Id("a"), Ascending, NullsFirst))
    }

    "translate ORDER BY a DESC" in {
      val tree = parseString("ORDER BY a DESC", _.orderByClause())
      astBuilder.buildSortOrder(tree) shouldBe Seq(SortOrder(Id("a"), Descending, NullsFirst))
    }

    "translate ORDER BY a, b DESC" in {
      val tree = parseString("ORDER BY a, b DESC", _.orderByClause())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(Id("a"), Ascending, NullsLast),
        SortOrder(Id("b"), Descending, NullsFirst))
    }

    "translate ORDER BY a DESC NULLS LAST, b" in {
      val tree = parseString("ORDER BY a DESC NULLS LAST, b", _.orderByClause())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(Id("a"), Descending, NullsLast),
        SortOrder(Id("b"), Ascending, NullsLast))
    }

    "translate ORDER BY with many expressions" in {
      val tree = parseString("ORDER BY a DESC, b, c ASC, d DESC NULLS LAST, e", _.orderByClause())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(Id("a"), Descending, NullsFirst),
        SortOrder(Id("b"), Ascending, NullsLast),
        SortOrder(Id("c"), Ascending, NullsLast),
        SortOrder(Id("d"), Descending, NullsLast),
        SortOrder(Id("e"), Ascending, NullsLast))
    }

    "translate EXISTS expressions" in {
      exampleExpr("EXISTS (SELECT * FROM t)", _.predicate, Exists(Project(namedTable("t"), Seq(Star(None)))))
    }

    // see https://github.com/databrickslabs/remorph/issues/273
    "translate NOT EXISTS expressions" ignore {
      exampleExpr("NOT EXISTS (SELECT * FROM t)", _.expr(), Not(Exists(Project(namedTable("t"), Seq(Star(None))))))
    }

  }

  "translate CASE expressions" in {
    exampleExpr(
      "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
      _.caseExpression(),
      Case(
        expression = None,
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Id("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Id("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = None))

    exampleExpr(
      "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
      _.caseExpression(),
      Case(
        expression = Some(Literal(string = Some("foo"))),
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Id("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Id("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = None))

    exampleExpr(
      "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
      _.caseExpression(),
      Case(
        expression = None,
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Id("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Id("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = Some(Literal(string = Some("other")))))

    exampleExpr(
      "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
      _.caseExpression(),
      Case(
        expression = Some(Literal(string = Some("foo"))),
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(Id("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(Id("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = Some(Literal(string = Some("other")))))

  }

  "SnowflakeExpressionBuilder.visit_Literal" should {
    "handle unresolved child" in {
      val literal = mock[LiteralContext]
      astBuilder.visitLiteral(literal) shouldBe Literal(nullType = Some(NullType))
      verify(literal).sign()
      verify(literal).DATE_LIT()
      verify(literal).TIMESTAMP_LIT()
      verify(literal).STRING()
      verify(literal).DECIMAL()
      verify(literal).FLOAT()
      verify(literal).REAL()
      verify(literal).trueFalse()
      verify(literal).NULL_()
      verify(literal).jsonLiteral()
      verify(literal).arrayLiteral()
      verifyNoMoreInteractions(literal)
    }
  }

  "SnowflakeExpressionBuilder.buildComparisonExpression" should {
    "handle unresolved child" in {
      val operator = mock[ComparisonOperatorContext]
      val dummyTextForOperator = "dummy"
      when(operator.getText).thenReturn(dummyTextForOperator)
      astBuilder.buildComparisonExpression(operator, null, null) shouldBe UnresolvedExpression(dummyTextForOperator)
      verify(operator).EQ()
      verify(operator).NE()
      verify(operator).LTGT()
      verify(operator).GT()
      verify(operator).LT()
      verify(operator).GE()
      verify(operator).LE()
      verify(operator).getText
      verifyNoMoreInteractions(operator)
    }
  }

}
