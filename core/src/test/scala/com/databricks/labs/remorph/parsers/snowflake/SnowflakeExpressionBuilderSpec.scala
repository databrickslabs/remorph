package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.IRHelpers
import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{ComparisonOperatorContext, LiteralContext, RankingWindowedFunctionContext}
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
      example("null", _.literal(), Literal(nullType = Some(NullType())))
      example("true", _.literal(), Literal(boolean = Some(true)))
      example("false", _.literal(), Literal(boolean = Some(false)))
      example("1", _.literal(), Literal(short = Some(1)))
      example(Int.MaxValue.toString, _.literal(), Literal(integer = Some(Int.MaxValue)))
      example("-1", _.literal(), Literal(short = Some(-1)))
      example("1.1", _.literal(), Literal(float = Some(1.1f)))
      example("1.1e2", _.literal(), Literal(short = Some(110)))
      example(Long.MaxValue.toString, _.literal(), Literal(long = Some(Long.MaxValue)))
      example("1.1e-2", _.literal(), Literal(float = Some(0.011f)))
      example("0.123456789", _.literal(), Literal(double = Some(0.123456789)))
      example("0.123456789e-1234", _.literal(), Literal(decimal = Some(Decimal("0.123456789e-1234", None, None))))
      example("'foo'", _.literal(), Literal(string = Some("foo")))
    }

    "translate column names" in {
      example("x", _.columnName(), simplyNamedColumn("x"))
    }

    "translate aggregation functions" in {
      example("COUNT(x)", _.aggregateFunction(), CallFunction("COUNT", Seq(simplyNamedColumn("x"))))
      example("AVG(x)", _.aggregateFunction(), CallFunction("AVG", Seq(simplyNamedColumn("x"))))
      example("SUM(x)", _.aggregateFunction(), CallFunction("SUM", Seq(simplyNamedColumn("x"))))
      example("MIN(x)", _.aggregateFunction(), CallFunction("MIN", Seq(simplyNamedColumn("x"))))

      example("COUNT(*)", _.aggregateFunction(), CallFunction("COUNT", Seq(Star(None))))

      example(
        "LISTAGG(x, ',')",
        _.aggregateFunction(),
        CallFunction("LISTAGG", Seq(simplyNamedColumn("x"), Literal(string = Some(",")))))
      example("ARRAY_AGG(x)", _.aggregateFunction(), CallFunction("ARRAYAGG", Seq(simplyNamedColumn("x"))))
    }

    "translate a query with a window function" in {

      example(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(simplyNamedColumn("a"), DescendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))

      example(
        query = "ROW_NUMBER() OVER (PARTITION BY a)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(simplyNamedColumn("a")),
          sort_order = Seq(),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))
      example(
        query = "NTILE(42) OVER (PARTITION BY a ORDER BY b, c DESC, d)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = NTile(Literal(short = Some(42))),
          partition_spec = Seq(simplyNamedColumn("a")),
          sort_order = Seq(
            SortOrder(simplyNamedColumn("b"), AscendingSortDirection, SortNullsLast),
            SortOrder(simplyNamedColumn("c"), DescendingSortDirection, SortNullsLast),
            SortOrder(simplyNamedColumn("d"), AscendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))
    }

    // see https://github.com/databrickslabs/remorph/issues/258
    "missing bits in window function grammar" ignore {

      // line 1:35 mismatched input 'NULLS' expecting {')', ','}
      example(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC NULLS FIRST)",
        rule = _.rankingWindowedFunction(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(simplyNamedColumn("a"), DescendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))

      // line 1:33 no viable alternative at input 'a ROWS'
      example(
        query = "ROW_NUMBER() OVER(PARTITION BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
        rule = _.rankingWindowedFunction(),
        expectedAst = null)
    }

    "translate star-expressions" in {
      example("*", _.columnElemStar(), Star(None))
      example("t.*", _.columnElemStar(), Star(Some(ObjectReference(Id("t")))))
    }
  }

  "SnowflakeExpressionBuilder.buildSortOrder" should {

    "translate ORDER BY a" in {
      val tree = parseString("ORDER BY a", _.orderByExpr())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(simplyNamedColumn("a"), AscendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a ASC" in {
      val tree = parseString("ORDER BY a ASC", _.orderByExpr())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(simplyNamedColumn("a"), AscendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a DESC" in {
      val tree = parseString("ORDER BY a DESC", _.orderByExpr())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(simplyNamedColumn("a"), DescendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a, b DESC" in {
      val tree = parseString("ORDER BY a, b DESC", _.orderByExpr())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(simplyNamedColumn("a"), AscendingSortDirection, SortNullsLast),
        SortOrder(simplyNamedColumn("b"), DescendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY a DESC, b" in {
      val tree = parseString("ORDER BY a DESC, b", _.orderByExpr())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(simplyNamedColumn("a"), DescendingSortDirection, SortNullsLast),
        SortOrder(simplyNamedColumn("b"), AscendingSortDirection, SortNullsLast))
    }

    "translate ORDER BY with many expressions" in {
      val tree = parseString("ORDER BY a DESC, b, c ASC, d DESC, e", _.orderByExpr())
      astBuilder.buildSortOrder(tree) shouldBe Seq(
        SortOrder(simplyNamedColumn("a"), DescendingSortDirection, SortNullsLast),
        SortOrder(simplyNamedColumn("b"), AscendingSortDirection, SortNullsLast),
        SortOrder(simplyNamedColumn("c"), AscendingSortDirection, SortNullsLast),
        SortOrder(simplyNamedColumn("d"), DescendingSortDirection, SortNullsLast),
        SortOrder(simplyNamedColumn("e"), AscendingSortDirection, SortNullsLast))
    }

    "translate EXISTS expressions" in {
      example("EXISTS (SELECT * FROM t)", _.predicate, Exists(Project(namedTable("t"), Seq(Star(None)))))
    }

    // see https://github.com/databrickslabs/remorph/issues/273
    "translate NOT EXISTS expressions" ignore {
      example("NOT EXISTS (SELECT * FROM t)", _.expr(), Not(Exists(Project(namedTable("t"), Seq(Star(None))))))
    }

  }

  "translate CASE expressions" in {
    example(
      "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
      _.caseExpression(),
      Case(
        expression = None,
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(simplyNamedColumn("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(simplyNamedColumn("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = None))

    example(
      "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
      _.caseExpression(),
      Case(
        expression = Some(Literal(string = Some("foo"))),
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(simplyNamedColumn("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(simplyNamedColumn("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = None))

    example(
      "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
      _.caseExpression(),
      Case(
        expression = None,
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(simplyNamedColumn("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(simplyNamedColumn("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = Some(Literal(string = Some("other")))))

    example(
      "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
      _.caseExpression(),
      Case(
        expression = Some(Literal(string = Some("foo"))),
        branches = scala.collection.immutable.Seq(
          WhenBranch(Equals(simplyNamedColumn("col1"), Literal(short = Some(1))), Literal(string = Some("one"))),
          WhenBranch(Equals(simplyNamedColumn("col2"), Literal(short = Some(2))), Literal(string = Some("two")))),
        otherwise = Some(Literal(string = Some("other")))))

  }

  "Unparsed input" should {
    "be reported as UnresolvedExpression" in {
      example("{'name':'Homer Simpson'}", _.jsonLiteral(), UnresolvedExpression("{'name':'Homer Simpson'}"))
    }
  }

  "SnowflakeExpressionBuilder.visit_Literal" should {
    "handle unresolved input" in {
      val literal = mock[LiteralContext]
      astBuilder.visitLiteral(literal) shouldBe Literal(nullType = Some(NullType()))
      verify(literal).sign()
      verify(literal).STRING()
      verify(literal).DECIMAL()
      verify(literal).FLOAT()
      verify(literal).REAL()
      verify(literal).trueFalse()
      verify(literal).NULL_()
      verifyNoMoreInteractions(literal)
    }
  }

  "SnowflakeExpressionBuilder.buildComparisonExpression" should {
    "handle unresolved input" in {
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

  "SnowflakeExpressionBuilder.buildWindowFunction" should {
    "handle unresolved input" in {
      val windowedFunction = mock[RankingWindowedFunctionContext]
      val dummyTextForWindowedFunction = "dummy"
      when(windowedFunction.getText).thenReturn(dummyTextForWindowedFunction)
      astBuilder.buildWindowFunction(windowedFunction) shouldBe UnresolvedExpression(dummyTextForWindowedFunction)
      verify(windowedFunction).ROW_NUMBER()
      verify(windowedFunction).NTILE()
      verify(windowedFunction).getText
      verifyNoMoreInteractions(windowedFunction)
    }
  }

}
