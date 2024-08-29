package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{ComparisonOperatorContext, LiteralContext}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
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
    "translate literals" should {
      "null" in {
        exampleExpr("null", _.literal(), Literal.Null)
      }
      "true" in {
        exampleExpr("true", _.literal(), Literal.True)
      }
      "false" in {
        exampleExpr("false", _.literal(), Literal.False)
      }
      "1" in {
        exampleExpr("1", _.literal(), Literal(1))
      }
      Int.MaxValue.toString in {
        exampleExpr(Int.MaxValue.toString, _.literal(), Literal(Int.MaxValue))
      }
      "-1" in {
        exampleExpr("-1", _.literal(), Literal(-1))
      }
      "1.1" in {
        exampleExpr("1.1", _.literal(), Literal(1.1f))
      }
      "1.1e2" in {
        exampleExpr("1.1e2", _.literal(), Literal(110))
      }
      Long.MaxValue.toString in {
        exampleExpr(Long.MaxValue.toString, _.literal(), Literal(Long.MaxValue))
      }
      "1.1e-2" in {
        exampleExpr("1.1e-2", _.literal(), Literal(0.011f))
      }
      "0.123456789" in {
        exampleExpr("0.123456789", _.literal(), Literal(0.123456789))
      }
      "0.123456789e-1234" in {
        exampleExpr("0.123456789e-1234", _.literal(), DecimalLiteral("0.123456789e-1234"))
      }
      "'foo'" in {
        exampleExpr("'foo'", _.literal(), Literal("foo"))
      }
      "DATE'1970-01-01'" in {
        exampleExpr("DATE'1970-01-01'", _.literal(), Literal(0, DateType))
      }
      "TIMESTAMP'1970-01-01 00:00:00'" in {
        exampleExpr("TIMESTAMP'1970-01-01 00:00:00'", _.literal(), Literal(0, TimestampType))
      }
    }

    "translate ids (quoted or not)" should {
      "foo" in {
        exampleExpr("foo", _.id(), Id("foo"))
      }
      "\"foo\"" in {
        exampleExpr("\"foo\"", _.id(), Id("foo", caseSensitive = true))
      }
      "\"foo \"\"quoted bar\"\"\"" in {
        exampleExpr("\"foo \"\"quoted bar\"\"\"", _.id(), Id("foo \"quoted bar\"", caseSensitive = true))
      }
    }

    "translate column names" should {
      "x" in {
        exampleExpr("x", _.columnName(), simplyNamedColumn("x"))
      }
      "\"My Table\".x" in {
        exampleExpr(
          "\"My Table\".x",
          _.columnName(),
          Column(Some(ObjectReference(Id("My Table", caseSensitive = true))), Id("x")))
      }
    }
    "translate aliases" should {
      "x AS y" in {
        exampleExpr("1 AS y", _.selectListElem(), Alias(Literal(1), Id("y")))
      }
      "1 y" in {
        exampleExpr("1 y", _.selectListElem(), Alias(Literal(1), Id("y")))
      }
    }

    "translate simple numeric binary expressions" should {
      "1 + 2" in {
        exampleExpr("1 + 2", _.expr(), ir.Add(ir.Literal(1), ir.Literal(2)))
      }
      "1 +2" in {
        exampleExpr("1 +2", _.expr(), ir.Add(ir.Literal(1), ir.Literal(2)))
      }
      "1 - 2" in {
        exampleExpr("1 - 2", _.expr(), ir.Subtract(ir.Literal(1), ir.Literal(2)))
      }
      "1 -2" in {
        exampleExpr("1 -2", _.expr(), ir.Subtract(ir.Literal(1), ir.Literal(2)))
      }
      "1 * 2" in {
        exampleExpr("1 * 2", _.expr(), ir.Multiply(ir.Literal(1), ir.Literal(2)))
      }
      "1 / 2" in {
        exampleExpr("1 / 2", _.expr(), ir.Divide(ir.Literal(1), ir.Literal(2)))
      }
      "1 % 2" in {
        exampleExpr("1 % 2", _.expr(), ir.Mod(ir.Literal(1), ir.Literal(2)))
      }
      "'A' || 'B'" in {
        exampleExpr("'A' || 'B'", _.expr(), ir.Concat(Seq(ir.Literal("A"), ir.Literal("B"))))
      }
    }

    "translate complex binary expressions" should {
      "a + b * 2" in {
        exampleExpr("a + b * 2", _.expr(), ir.Add(Id("a"), ir.Multiply(Id("b"), ir.Literal(2))))
      }
      "(a + b) * 2" in {
        exampleExpr("(a + b) * 2", _.expr(), ir.Multiply(ir.Add(Id("a"), Id("b")), ir.Literal(2)))
      }
      "a % 3 + b * 2 - c / 5" in {
        exampleExpr(
          "a % 3 + b * 2 - c / 5",
          _.expr(),
          ir.Subtract(
            ir.Add(ir.Mod(Id("a"), ir.Literal(3)), ir.Multiply(Id("b"), ir.Literal(2))),
            ir.Divide(Id("c"), ir.Literal(5))))
      }
      "a || b || c" in {
        exampleExpr("a || b || c", _.expr(), ir.Concat(Seq(ir.Concat(Seq(Id("a"), Id("b"))), Id("c"))))
      }
    }

    "correctly apply operator precedence and associativity" should {
      "1 + -++-2" in {
        exampleExpr(
          "1 + -++-2",
          _.expr(),
          ir.Add(ir.Literal(1), ir.UMinus(ir.UPlus(ir.UPlus(ir.UMinus(ir.Literal(2)))))))
      }
      "1 + -2 * 3" in {
        exampleExpr("1 + -2 * 3", _.expr(), ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))))
      }
      "1 + -2 * 3 + 7 || 'leeds1' || 'leeds2' || 'leeds3'" in {
        exampleExpr(
          "1 + -2 * 3 + 7 || 'leeds1' || 'leeds2' || 'leeds3'",
          _.expr(),
          ir.Concat(
            Seq(
              ir.Concat(Seq(
                ir.Concat(Seq(
                  ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))), ir.Literal(7)),
                  ir.Literal("leeds1"))),
                ir.Literal("leeds2"))),
              ir.Literal("leeds3"))))
      }
    }

    "correctly respect explicit precedence with parentheses" should {
      "(1 + 2) * 3" in {
        exampleExpr("(1 + 2) * 3", _.expr(), ir.Multiply(ir.Add(ir.Literal(1), ir.Literal(2)), ir.Literal(3)))
      }
      "1 + (2 * 3)" in {
        exampleExpr("1 + (2 * 3)", _.expr(), ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Literal(3))))
      }
      "(1 + 2) * (3 + 4)" in {
        exampleExpr(
          "(1 + 2) * (3 + 4)",
          _.expr(),
          ir.Multiply(ir.Add(ir.Literal(1), ir.Literal(2)), ir.Add(ir.Literal(3), ir.Literal(4))))
      }
      "1 + (2 * 3) + 4" in {
        exampleExpr(
          "1 + (2 * 3) + 4",
          _.expr(),
          ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Literal(3))), ir.Literal(4)))
      }
      "1 + (2 * 3 + 4)" in {
        exampleExpr(
          "1 + (2 * 3 + 4)",
          _.expr(),
          ir.Add(ir.Literal(1), ir.Add(ir.Multiply(ir.Literal(2), ir.Literal(3)), ir.Literal(4))))
      }
      "1 + (2 * (3 + 4))" in {
        exampleExpr(
          "1 + (2 * (3 + 4))",
          _.expr(),
          ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Add(ir.Literal(3), ir.Literal(4)))))
      }
      "(1 + (2 * (3 + 4)))" in {
        exampleExpr(
          "(1 + (2 * (3 + 4)))",
          _.expr(),
          ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Add(ir.Literal(3), ir.Literal(4)))))
      }
    }

    "translate functions with special syntax" should {
      "EXTRACT(day FROM date1)" in {
        exampleExpr(
          "EXTRACT(day FROM date1)",
          _.builtinFunction(),
          CallFunction("EXTRACT", Seq(Id("day"), Id("date1"))))
      }

      "EXTRACT('day' FROM date1)" in {
        exampleExpr(
          "EXTRACT('day' FROM date1)",
          _.builtinFunction(),
          CallFunction("EXTRACT", Seq(Id("day"), Id("date1"))))
      }

    }

    "translate functions named with a keyword" should {
      "LEFT(foo, bar)" in {
        exampleExpr("LEFT(foo, bar)", _.standardFunction(), CallFunction("LEFT", Seq(Id("foo"), Id("bar"))))
      }
      "RIGHT(foo, bar)" in {
        exampleExpr("RIGHT(foo, bar)", _.standardFunction(), CallFunction("RIGHT", Seq(Id("foo"), Id("bar"))))
      }
    }

    "translate aggregation functions" should {
      "COUNT(x)" in {
        exampleExpr("COUNT(x)", _.aggregateFunction(), CallFunction("COUNT", Seq(Id("x"))))
      }
      "AVG(x)" in {
        exampleExpr("AVG(x)", _.aggregateFunction(), CallFunction("AVG", Seq(Id("x"))))
      }
      "SUM(x)" in {
        exampleExpr("SUM(x)", _.aggregateFunction(), CallFunction("SUM", Seq(Id("x"))))
      }
      "MIN(x)" in {
        exampleExpr("MIN(x)", _.aggregateFunction(), CallFunction("MIN", Seq(Id("x"))))
      }
      "COUNT(*)" in {
        exampleExpr("COUNT(*)", _.aggregateFunction(), CallFunction("COUNT", Seq(Star(None))))
      }
      "LISTAGG(x, ',')" in {
        exampleExpr("LISTAGG(x, ',')", _.aggregateFunction(), CallFunction("LISTAGG", Seq(Id("x"), Literal(","))))
      }
      "ARRAY_AGG(x)" in {
        exampleExpr("ARRAY_AGG(x)", _.aggregateFunction(), CallFunction("ARRAY_AGG", Seq(Id("x"))))
      }
    }

    "translate a query with a window function" should {
      "ROW_NUMBER() OVER (ORDER BY a DESC)" in {
        exampleExpr(
          "ROW_NUMBER() OVER (ORDER BY a DESC)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("ROW_NUMBER", Seq()),
            partition_spec = Seq(),
            sort_order = Seq(SortOrder(Id("a"), Descending, NullsFirst)),
            frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, UnboundedFollowing))))
      }
      "ROW_NUMBER() OVER (PARTITION BY a)" in {
        exampleExpr(
          "ROW_NUMBER() OVER (PARTITION BY a)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("ROW_NUMBER", Seq()),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(),
            frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, UnboundedFollowing))))
      }
      "NTILE(42) OVER (PARTITION BY a ORDER BY b, c DESC, d)" in {
        exampleExpr(
          "NTILE(42) OVER (PARTITION BY a ORDER BY b, c DESC, d)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("NTILE", Seq(Literal(42))),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(
              SortOrder(Id("b"), Ascending, NullsLast),
              SortOrder(Id("c"), Descending, NullsFirst),
              SortOrder(Id("d"), Ascending, NullsLast)),
            frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, UnboundedFollowing))))
      }
      "LAST_VALUE(col_name) IGNORE NULLS OVER (PARTITION BY a ORDER BY b, c DESC, d)" in {
        exampleExpr(
          "LAST_VALUE(col_name) IGNORE NULLS OVER (PARTITION BY a ORDER BY b, c DESC, d)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("LAST_VALUE", Seq(Id("col_name", false))),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(
              SortOrder(Id("b"), Ascending, NullsLast),
              SortOrder(Id("c"), Descending, NullsFirst),
              SortOrder(Id("d"), Ascending, NullsLast)),
            frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, UnboundedFollowing)),
            ignore_nulls = true))
      }
    }

    "translate window frame specifications" should {
      "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)" in {
        exampleExpr(
          "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("ROW_NUMBER", Seq()),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
            frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, CurrentRow))))
      }
      "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)" in {
        exampleExpr(
          "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("ROW_NUMBER", Seq()),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
            frame_spec = Some(WindowFrame(RowsFrame, UnboundedPreceding, UnboundedFollowing))))
      }
      "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN 42 PRECEDING AND CURRENT ROW)" in {
        exampleExpr(
          "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN 42 PRECEDING AND CURRENT ROW)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("ROW_NUMBER", Seq()),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
            frame_spec = Some(WindowFrame(RowsFrame, PrecedingN(Literal(42)), CurrentRow))))
      }
      "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN 42 PRECEDING AND 42 FOLLOWING)" in {
        exampleExpr(
          "ROW_NUMBER() OVER(PARTITION BY a ORDER BY a ROWS BETWEEN 42 PRECEDING AND 42 FOLLOWING)",
          _.rankingWindowedFunction(),
          expectedAst = Window(
            window_function = CallFunction("ROW_NUMBER", Seq()),
            partition_spec = Seq(Id("a")),
            sort_order = Seq(SortOrder(Id("a"), Ascending, NullsLast)),
            frame_spec = Some(WindowFrame(RowsFrame, PrecedingN(Literal(42)), FollowingN(Literal(42))))))
      }
    }

    "translate star-expressions" should {
      "*" in {
        exampleExpr("*", _.columnElemStar(), Star(None))
      }
      "t.*" in {
        exampleExpr("t.*", _.columnElemStar(), Star(Some(ObjectReference(Id("t")))))
      }
      exampleExpr(
        "db1.schema1.table1.*",
        _.columnElemStar(),
        Star(Some(ObjectReference(Id("db1"), Id("schema1"), Id("table1")))))
    }

    "translate scalar subquery" in {
      exampleExpr(
        query = "(SELECT col1 from table_expr)",
        rule = _.expr(),
        expectedAst = ScalarSubquery(Project(namedTable("table_expr"), Seq(Column(None, Id("col1"))))))
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

  "translate CASE expressions" should {
    "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END" in {
      exampleExpr(
        "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
        _.caseExpression(),
        Case(
          expression = None,
          branches = scala.collection.immutable.Seq(
            WhenBranch(Equals(Id("col1"), Literal(1)), Literal("one")),
            WhenBranch(Equals(Id("col2"), Literal(2)), Literal("two"))),
          otherwise = None))
    }
    "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END" in {
      exampleExpr(
        "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' END",
        _.caseExpression(),
        Case(
          expression = Some(Literal("foo")),
          branches = scala.collection.immutable.Seq(
            WhenBranch(Equals(Id("col1"), Literal(1)), Literal("one")),
            WhenBranch(Equals(Id("col2"), Literal(2)), Literal("two"))),
          otherwise = None))
    }
    "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END" in {
      exampleExpr(
        "CASE WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
        _.caseExpression(),
        Case(
          expression = None,
          branches = scala.collection.immutable.Seq(
            WhenBranch(Equals(Id("col1"), Literal(1)), Literal("one")),
            WhenBranch(Equals(Id("col2"), Literal(2)), Literal("two"))),
          otherwise = Some(Literal("other"))))
    }
    "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END" in {
      exampleExpr(
        "CASE 'foo' WHEN col1 = 1 THEN 'one' WHEN col2 = 2 THEN 'two' ELSE 'other' END",
        _.caseExpression(),
        Case(
          expression = Some(Literal("foo")),
          branches = scala.collection.immutable.Seq(
            WhenBranch(Equals(Id("col1"), Literal(1)), Literal("one")),
            WhenBranch(Equals(Id("col2"), Literal(2)), Literal("two"))),
          otherwise = Some(Literal("other"))))
    }
  }

  "SnowflakeExpressionBuilder.visit_Literal" should {
    "handle unresolved child" in {
      val literal = mock[LiteralContext]
      astBuilder.visitLiteral(literal) shouldBe Literal.Null
      verify(literal).sign()
      verify(literal).DATE_LIT()
      verify(literal).TIMESTAMP_LIT()
      verify(literal).string()
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

  // Note that when we truly handle &vars, we will get ir.Variable here and not Id
  // and the & parts will not be changed to ${} until we get to the final SQL generation
  // but we are in a half way house transition state
  "variable substitution" should {
    "&abc" in {
      exampleExpr("&abc", _.expr(), Id("$abc"))
    }
    "&ab_c.bc_d" in {
      exampleExpr("&ab_c.bc_d", _.expr(), Dot(Id("$ab_c"), Id("bc_d")))
    }
    "&{ab_c}.&bc_d" in {
      exampleExpr("&{ab_c}.&bc_d", _.expr(), Dot(Id("$ab_c"), Id("$bc_d")))
    }
  }
}
