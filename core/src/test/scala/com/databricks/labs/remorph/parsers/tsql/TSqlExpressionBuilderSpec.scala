package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.ID
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.tree.TerminalNodeImpl
import org.antlr.v4.runtime.{CommonToken, Token}
import org.mockito.ArgumentMatchers.{any, anyInt}
import org.mockito.Mockito.{mock, when}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlExpressionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with ir.IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = vc.expressionBuilder

  "TSqlExpressionBuilder" should {
    "translate literals" in {
      exampleExpr("null", _.expression(), ir.Literal.Null)
      exampleExpr("1", _.expression(), ir.Literal(1))
      exampleExpr("-1", _.expression(), ir.UMinus(ir.Literal(1))) // TODO: add optimizer
      exampleExpr("+1", _.expression(), ir.UPlus(ir.Literal(1)))
      exampleExpr("1.1", _.expression(), ir.Literal(1.1f))
      exampleExpr("'foo'", _.expression(), ir.Literal("foo"))
    }
    "translate scientific notation" in {
      exampleExpr("1.1e2", _.expression(), ir.Literal(110))
      exampleExpr("1.1e-2", _.expression(), ir.Literal(0.011f))
      exampleExpr("1e2", _.expression(), ir.Literal(100))
      exampleExpr("0.123456789", _.expression(), ir.Literal(0.123456789))
      exampleExpr("0.123456789e-1234", _.expression(), ir.DecimalLiteral("0.123456789e-1234"))
    }
    "translate simple primitives" in {
      exampleExpr("DEFAULT", _.expression(), Default())
      exampleExpr("@LocalId", _.expression(), ir.Identifier("@LocalId", isQuoted = false))
    }

    "translate simple numeric binary expressions" in {
      exampleExpr("1 + 2", _.expression(), ir.Add(ir.Literal(1), ir.Literal(2)))
      exampleExpr("1 +2", _.expression(), ir.Add(ir.Literal(1), ir.Literal(2)))
      exampleExpr("1 - 2", _.expression(), ir.Subtract(ir.Literal(1), ir.Literal(2)))
      exampleExpr("1 -2", _.expression(), ir.Subtract(ir.Literal(1), ir.Literal(2)))
      exampleExpr("1 * 2", _.expression(), ir.Multiply(ir.Literal(1), ir.Literal(2)))
      exampleExpr("1 / 2", _.expression(), ir.Divide(ir.Literal(1), ir.Literal(2)))
      exampleExpr("1 % 2", _.expression(), ir.Mod(ir.Literal(1), ir.Literal(2)))
      exampleExpr("'A' || 'B'", _.expression(), ir.Concat(Seq(ir.Literal("A"), ir.Literal("B"))))
      exampleExpr("4 ^ 2", _.expression(), ir.BitwiseXor(ir.Literal(4), ir.Literal(2)))
    }
    "translate complex binary expressions" in {
      exampleExpr(
        "a + b * 2",
        _.expression(),
        ir.Add(simplyNamedColumn("a"), ir.Multiply(simplyNamedColumn("b"), ir.Literal(2))))
      exampleExpr(
        "(a + b) * 2",
        _.expression(),
        ir.Multiply(ir.Add(simplyNamedColumn("a"), simplyNamedColumn("b")), ir.Literal(2)))
      exampleExpr(
        "a & b | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(simplyNamedColumn("a"), simplyNamedColumn("b")), simplyNamedColumn("c")))
      exampleExpr(
        "(a & b) | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(simplyNamedColumn("a"), simplyNamedColumn("b")), simplyNamedColumn("c")))
      exampleExpr(
        "a + b * 2",
        _.expression(),
        ir.Add(simplyNamedColumn("a"), ir.Multiply(simplyNamedColumn("b"), ir.Literal(2))))
      exampleExpr(
        "(a + b) * 2",
        _.expression(),
        ir.Multiply(ir.Add(simplyNamedColumn("a"), simplyNamedColumn("b")), ir.Literal(2)))
      exampleExpr(
        "a & b | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(simplyNamedColumn("a"), simplyNamedColumn("b")), simplyNamedColumn("c")))
      exampleExpr(
        "(a & b) | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(simplyNamedColumn("a"), simplyNamedColumn("b")), simplyNamedColumn("c")))
      exampleExpr(
        "a % 3 + b * 2 - c / 5",
        _.expression(),
        ir.Subtract(
          ir.Add(ir.Mod(simplyNamedColumn("a"), ir.Literal(3)), ir.Multiply(simplyNamedColumn("b"), ir.Literal(2))),
          ir.Divide(simplyNamedColumn("c"), ir.Literal(5))))
      exampleExpr(
        query = "a || b || c",
        _.expression(),
        ir.Concat(Seq(ir.Concat(Seq(simplyNamedColumn("a"), simplyNamedColumn("b"))), simplyNamedColumn("c"))))
    }
    "correctly apply operator precedence and associativity" in {
      exampleExpr(
        "1 + -++-2",
        _.expression(),
        ir.Add(ir.Literal(1), ir.UMinus(ir.UPlus(ir.UPlus(ir.UMinus(ir.Literal(2)))))))
      exampleExpr(
        "1 + ~ 2 * 3",
        _.expression(),
        ir.Add(ir.Literal(1), ir.Multiply(ir.BitwiseNot(ir.Literal(2)), ir.Literal(3))))
      exampleExpr(
        "1 + -2 * 3",
        _.expression(),
        ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))))
      exampleExpr(
        "1 + -2 * 3 + 7 & 66",
        _.expression(),
        ir.BitwiseAnd(
          ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))), ir.Literal(7)),
          ir.Literal(66)))
      exampleExpr(
        "1 + -2 * 3 + 7 ^ 66",
        _.expression(),
        ir.BitwiseXor(
          ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))), ir.Literal(7)),
          ir.Literal(66)))
      exampleExpr(
        "1 + -2 * 3 + 7 | 66",
        _.expression(),
        ir.BitwiseOr(
          ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))), ir.Literal(7)),
          ir.Literal(66)))
      exampleExpr(
        "1 + -2 * 3 + 7 + ~66",
        _.expression(),
        ir.Add(
          ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))), ir.Literal(7)),
          ir.BitwiseNot(ir.Literal(66))))
      exampleExpr(
        "1 + -2 * 3 + 7 | 1980 || 'leeds1' || 'leeds2' || 'leeds3'",
        _.expression(),
        ir.Concat(
          Seq(
            ir.Concat(Seq(
              ir.Concat(
                Seq(
                  ir.BitwiseOr(
                    ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.UMinus(ir.Literal(2)), ir.Literal(3))), ir.Literal(7)),
                    ir.Literal(1980)),
                  ir.Literal("leeds1"))),
              ir.Literal("leeds2"))),
            ir.Literal("leeds3"))))
    }
    "correctly respect explicit precedence with parentheses" in {
      exampleExpr("(1 + 2) * 3", _.expression(), ir.Multiply(ir.Add(ir.Literal(1), ir.Literal(2)), ir.Literal(3)))
      exampleExpr("1 + (2 * 3)", _.expression(), ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Literal(3))))
      exampleExpr(
        "(1 + 2) * (3 + 4)",
        _.expression(),
        ir.Multiply(ir.Add(ir.Literal(1), ir.Literal(2)), ir.Add(ir.Literal(3), ir.Literal(4))))
      exampleExpr(
        "1 + (2 * 3) + 4",
        _.expression(),
        ir.Add(ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Literal(3))), ir.Literal(4)))
      exampleExpr(
        "1 + (2 * 3 + 4)",
        _.expression(),
        ir.Add(ir.Literal(1), ir.Add(ir.Multiply(ir.Literal(2), ir.Literal(3)), ir.Literal(4))))
      exampleExpr(
        "1 + (2 * (3 + 4))",
        _.expression(),
        ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Add(ir.Literal(3), ir.Literal(4)))))
      exampleExpr(
        "(1 + (2 * (3 + 4)))",
        _.expression(),
        ir.Add(ir.Literal(1), ir.Multiply(ir.Literal(2), ir.Add(ir.Literal(3), ir.Literal(4)))))
    }

    "correctly resolve dot delimited plain references" in {
      exampleExpr("a", _.expression(), simplyNamedColumn("a"))
      exampleExpr("a.b", _.expression(), ir.Column(Some(ir.ObjectReference(ir.Id("a"))), ir.Id("b")))
      exampleExpr("a.b.c", _.expression(), ir.Column(Some(ir.ObjectReference(ir.Id("a"), ir.Id("b"))), ir.Id("c")))
    }

    "correctly resolve RAW identifiers" in {
      exampleExpr("RAW", _.expression(), simplyNamedColumn("RAW"))
    }

    "correctly resolve # identifiers" in {
      exampleExpr("#RAW", _.expression(), simplyNamedColumn("#RAW"))
    }

    "correctly resolve \" quoted identifiers" in {
      exampleExpr("\"a\"", _.expression(), ir.Column(None, ir.Id("a", caseSensitive = true)))
    }

    "correctly resolve [] quoted identifiers" in {
      exampleExpr("[a]", _.expression(), ir.Column(None, ir.Id("a", caseSensitive = true)))
    }

    "correctly resolve [] quoted dot identifiers" in {
      exampleExpr(
        "[a].[b]",
        _.expression(),
        ir.Column(Some(ir.ObjectReference(ir.Id("a", caseSensitive = true))), ir.Id("b", caseSensitive = true)))
    }

    "correctly resolve [] quoted triple dot identifiers" in {
      exampleExpr(
        "[a].[b].[c]",
        _.expression(),
        ir.Column(
          Some(ir.ObjectReference(ir.Id("a", caseSensitive = true), ir.Id("b", caseSensitive = true))),
          ir.Id("c", caseSensitive = true)))
    }

    "correctly resolve keywords used as identifiers" in {
      exampleExpr("ABORT", _.expression(), simplyNamedColumn("ABORT"))
    }

    "translate a simple column" in {
      exampleExpr("a", _.selectListElem(), simplyNamedColumn("a"))
      exampleExpr("#a", _.selectListElem(), simplyNamedColumn("#a"))
      exampleExpr("[a]", _.selectListElem(), ir.Column(None, ir.Id("a", caseSensitive = true)))
      exampleExpr("\"a\"", _.selectListElem(), ir.Column(None, ir.Id("a", caseSensitive = true)))
      exampleExpr("RAW", _.selectListElem(), simplyNamedColumn("RAW"))
    }

    "translate a column with a table" in {
      exampleExpr("table_x.a", _.selectListElem(), ir.Column(Some(ir.ObjectReference(ir.Id("table_x"))), ir.Id("a")))
    }

    "translate a column with a schema" in {
      exampleExpr(
        "schema1.table_x.a",
        _.selectListElem(),
        ir.Column(Some(ir.ObjectReference(ir.Id("schema1"), ir.Id("table_x"))), ir.Id("a")))
    }

    "translate a column with a database" in {
      exampleExpr(
        "database1.schema1.table_x.a",
        _.selectListElem(),
        ir.Column(Some(ir.ObjectReference(ir.Id("database1"), ir.Id("schema1"), ir.Id("table_x"))), ir.Id("a")))
    }

    "translate a column with a server" in {
      exampleExpr(
        "server1..schema1.table_x.a",
        _.fullColumnName(),
        ir.Column(Some(ir.ObjectReference(ir.Id("server1"), ir.Id("schema1"), ir.Id("table_x"))), ir.Id("a")))
    }

    "translate a column without a table reference" in {
      exampleExpr("a", _.fullColumnName(), simplyNamedColumn("a"))
    }

    "return ir.Dot for otherwise unhandled DotExpr" in {
      val mockDotExprCtx = mock(classOf[TSqlParser.ExprDotContext])
      val mockExpressionCtx = mock(classOf[TSqlParser.ExpressionContext])
      val mockVisitor = mock(classOf[TSqlExpressionBuilder])

      when(mockDotExprCtx.expression(anyInt())).thenReturn(mockExpressionCtx)
      when(mockExpressionCtx.accept(mockVisitor)).thenReturn(ir.Literal("a"))
      val result = astBuilder.visitExprDot(mockDotExprCtx)

      result shouldBe a[ir.Dot]
    }

    "translate search conditions" in {
      exampleExpr("a = b", _.searchCondition(), ir.Equals(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a > b", _.searchCondition(), ir.GreaterThan(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a < b", _.searchCondition(), ir.LessThan(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a >= b", _.searchCondition(), ir.GreaterThanOrEqual(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a !< b", _.searchCondition(), ir.GreaterThanOrEqual(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a <= b", _.searchCondition(), ir.LessThanOrEqual(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a !> b", _.searchCondition(), ir.LessThanOrEqual(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a > = b", _.searchCondition(), ir.GreaterThanOrEqual(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a <  = b", _.searchCondition(), ir.LessThanOrEqual(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a <> b", _.searchCondition(), ir.NotEquals(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("a != b", _.searchCondition(), ir.NotEquals(simplyNamedColumn("a"), simplyNamedColumn("b")))
      exampleExpr("NOT a = b", _.searchCondition(), ir.Not(ir.Equals(simplyNamedColumn("a"), simplyNamedColumn("b"))))
      exampleExpr(
        "a = b AND c = e",
        _.searchCondition(),
        ir.And(
          ir.Equals(simplyNamedColumn("a"), simplyNamedColumn("b")),
          ir.Equals(simplyNamedColumn("c"), simplyNamedColumn("e"))))
      exampleExpr(
        "a = b OR c = e",
        _.searchCondition(),
        ir.Or(
          ir.Equals(simplyNamedColumn("a"), simplyNamedColumn("b")),
          ir.Equals(simplyNamedColumn("c"), simplyNamedColumn("e"))))
      exampleExpr(
        "a = b AND c = x OR e = f",
        _.searchCondition(),
        ir.Or(
          ir.And(
            ir.Equals(simplyNamedColumn("a"), simplyNamedColumn("b")),
            ir.Equals(simplyNamedColumn("c"), simplyNamedColumn("x"))),
          ir.Equals(simplyNamedColumn("e"), simplyNamedColumn("f"))))
      exampleExpr(
        "a = b AND (c = x OR e = f)",
        _.searchCondition(),
        ir.And(
          ir.Equals(simplyNamedColumn("a"), simplyNamedColumn("b")),
          ir.Or(
            ir.Equals(simplyNamedColumn("c"), simplyNamedColumn("x")),
            ir.Equals(simplyNamedColumn("e"), simplyNamedColumn("f")))))
    }

    "handle non special functions used in dot operators" in {
      exampleExpr(
        "a.b()",
        _.expression(),
        ir.Dot(
          simplyNamedColumn("a"),
          ir.UnresolvedFunction(
            "b",
            List(),
            is_distinct = false,
            is_user_defined_function = false,
            ruleText = "b(...)",
            ruleName = "N/A",
            tokenName = Some("N/A"),
            message = "Function b is not convertible to Databricks SQL")))
      exampleExpr(
        "a.b.c()",
        _.expression(),
        ir.Dot(
          simplyNamedColumn("a"),
          ir.Dot(
            simplyNamedColumn("b"),
            ir.UnresolvedFunction(
              "c",
              List(),
              is_distinct = false,
              is_user_defined_function = false,
              ruleText = "c(...)",
              ruleName = "N/A",
              tokenName = Some("N/A"),
              message = "Function c is not convertible to Databricks SQL"))))
      exampleExpr(
        "a.b.c.FLOOR(c)",
        _.expression(),
        ir.Dot(
          simplyNamedColumn("a"),
          ir.Dot(
            simplyNamedColumn("b"),
            ir.Dot(simplyNamedColumn("c"), ir.CallFunction("FLOOR", Seq(simplyNamedColumn("c")))))))
    }

    "handle unknown functions used with dots" in {
      exampleExpr(
        "a.UNKNOWN_FUNCTION()",
        _.expression(),
        ir.Dot(
          simplyNamedColumn("a"),
          ir.UnresolvedFunction(
            "UNKNOWN_FUNCTION",
            List(),
            is_distinct = false,
            is_user_defined_function = false,
            ruleText = "UNKNOWN_FUNCTION(...)",
            ruleName = "N/A",
            tokenName = Some("N/A"),
            message = "Function UNKNOWN_FUNCTION is not convertible to Databricks SQL")))
    }

    "cover case that cannot happen with dot" in {

      val mockCtx = mock(classOf[TSqlParser.ExprDotContext])
      val expressionMockColumn = mock(classOf[TSqlParser.ExpressionContext])
      when(mockCtx.expression(0)).thenReturn(expressionMockColumn)
      when(expressionMockColumn.accept(any())).thenReturn(simplyNamedColumn("a"))
      val expressionMockFunc = mock(classOf[TSqlParser.ExpressionContext])
      when(mockCtx.expression(1)).thenReturn(expressionMockFunc)
      when(expressionMockFunc.accept(any())).thenReturn(ir.CallFunction("UNKNOWN_FUNCTION", List()))
      val result = vc.expressionBuilder.visitExprDot(mockCtx)
      result shouldBe a[ir.Dot]
    }

    "translate case/when/else expressions" in {
      // Case with an initial expression and an else clause
      exampleExpr(
        "CASE a WHEN 1 THEN 'one' WHEN 2 THEN 'two' ELSE 'other' END",
        _.expression(),
        ir.Case(
          Some(simplyNamedColumn("a")),
          Seq(ir.WhenBranch(ir.Literal(1), ir.Literal("one")), ir.WhenBranch(ir.Literal(2), ir.Literal("two"))),
          Some(ir.Literal("other"))))

      // Case without an initial expression and with an else clause
      exampleExpr(
        "CASE WHEN a = 1 THEN 'one' WHEN a = 2 THEN 'two' ELSE 'other' END",
        _.expression(),
        ir.Case(
          None,
          Seq(
            ir.WhenBranch(ir.Equals(simplyNamedColumn("a"), ir.Literal(1)), ir.Literal("one")),
            ir.WhenBranch(ir.Equals(simplyNamedColumn("a"), ir.Literal(2)), ir.Literal("two"))),
          Some(ir.Literal("other"))))

      // Case with an initial expression and without an else clause
      exampleExpr(
        "CASE a WHEN 1 THEN 'one' WHEN 2 THEN 'two' END",
        _.expression(),
        ir.Case(
          Some(simplyNamedColumn("a")),
          Seq(ir.WhenBranch(ir.Literal(1), ir.Literal("one")), ir.WhenBranch(ir.Literal(2), ir.Literal("two"))),
          None))

      // Case without an initial expression and without an else clause
      exampleExpr(
        "CASE WHEN a = 1 AND b < 7 THEN 'one' WHEN a = 2 THEN 'two' END",
        _.expression(),
        ir.Case(
          None,
          Seq(
            ir.WhenBranch(
              ir.And(
                ir.Equals(simplyNamedColumn("a"), ir.Literal(1)),
                ir.LessThan(simplyNamedColumn("b"), ir.Literal(7))),
              ir.Literal("one")),
            ir.WhenBranch(ir.Equals(simplyNamedColumn("a"), ir.Literal(2)), ir.Literal("two"))),
          None))
    }

    "translate the $ACTION special column reference" in {
      exampleExpr("$ACTION", _.expression(), ir.DollarAction)
    }

    "translate a timezone reference" in {
      exampleExpr("a AT TIME ZONE 'UTC'", _.expression(), ir.Timezone(simplyNamedColumn("a"), ir.Literal("UTC")))
    }

    "return UnresolvedExpression for unsupported SelectListElem" in {

      val mockCtx = mock(classOf[TSqlParser.SelectListElemContext])

      // Ensure that both asterisk() and expressionElem() methods return null
      when(mockCtx.asterisk()).thenReturn(null)
      when(mockCtx.expressionElem()).thenReturn(null)
      val startTok = new CommonToken(ID, "s")
      when(mockCtx.getStart).thenReturn(startTok)
      when(mockCtx.getStop).thenReturn(startTok)
      when(mockCtx.getRuleIndex).thenReturn(SnowflakeParser.RULE_constraintAction)

      // Call the method with the mock instance
      val result = vc.expressionBuilder.buildSelectListElem(mockCtx)

      // Verify the result
      result shouldBe a[Seq[_]]
    }

    "cover default case in buildLocalAssign via visitSelectListElem" in {
      val selectListElemContextMock = mock(classOf[TSqlParser.SelectListElemContext])
      val eofToken = new CommonToken(Token.EOF)
      selectListElemContextMock.op = eofToken
      when(selectListElemContextMock.LOCAL_ID()).thenReturn(new TerminalNodeImpl(eofToken))
      when(selectListElemContextMock.asterisk()).thenReturn(null)
      when(selectListElemContextMock.getText).thenReturn("")

      val expressionContextMock = mock(classOf[TSqlParser.ExpressionContext])
      when(expressionContextMock.accept(any())).thenReturn(null)
      when(selectListElemContextMock.expression()).thenReturn(expressionContextMock)

      val result = vc.expressionBuilder.buildSelectListElem(selectListElemContextMock)

      result shouldBe a[Seq[_]]
    }

    "translate CAST(a AS tinyint)" in {
      exampleExpr("CAST(a AS tinyint)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.ByteType(size = Some(1))))
    }
    "translate CAST(a AS smallint)" in {
      exampleExpr("CAST(a AS smallint)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.ShortType))
    }
    "translate CAST(a AS INT)" in {
      exampleExpr("CAST(a AS INT)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.IntegerType))
    }
    "translate CAST(a AS bigint)" in {
      exampleExpr("CAST(a AS bigint)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.LongType))
    }
    "translate CAST(a AS bit)" in {
      exampleExpr("CAST(a AS bit)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.BooleanType))
    }
    "translate CAST(a AS money)" in {
      exampleExpr(
        "CAST(a AS money)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(19), Some(4))))
    }
    "translate CAST(a AS smallmoney)" in {
      exampleExpr(
        "CAST(a AS smallmoney)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), Some(4))))
    }
    "translate CAST(a AS float)" in {
      exampleExpr("CAST(a AS float)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.FloatType))
    }
    "translate CAST(a AS real)" in {
      exampleExpr("CAST(a AS real)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.DoubleType))
    }
    "translate CAST(a AS date)" in {
      exampleExpr("CAST(a AS date)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.DateType))
    }
    "translate CAST(a AS time)" in {
      exampleExpr("CAST(a AS time)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.TimeType))
    }
    "translate CAST(a AS datetime)" in {
      exampleExpr("CAST(a AS datetime)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.TimestampType))
    }
    "translate CAST(a AS datetime2)" in {
      exampleExpr("CAST(a AS datetime2)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.TimestampType))
    }
    "translate CAST(a AS datetimeoffset)" in {
      exampleExpr("CAST(a AS datetimeoffset)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.StringType))
    }
    "translate CAST(a AS smalldatetime)" in {
      exampleExpr("CAST(a AS smalldatetime)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.TimestampType))
    }
    "translate CAST(a AS char)" in {
      exampleExpr("CAST(a AS char)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.CharType(size = None)))
    }
    "translate CAST(a AS varchar)" in {
      exampleExpr("CAST(a AS varchar)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = None)))
    }
    "translate CAST(a AS nchar)" in {
      exampleExpr("CAST(a AS nchar)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.CharType(size = None)))
    }
    "translate CAST(a AS nvarchar)" in {
      exampleExpr("CAST(a AS nvarchar)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = None)))
    }
    "translate CAST(a AS text)" in {
      exampleExpr("CAST(a AS text)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.VarcharType(None)))
    }
    "translate CAST(a AS ntext)" in {
      exampleExpr("CAST(a AS ntext)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.VarcharType(None)))
    }
    "translate CAST(a AS image)" in {
      exampleExpr("CAST(a AS image)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.BinaryType))
    }
    "translate CAST(a AS decimal)" in {
      exampleExpr("CAST(a AS decimal)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.DecimalType(None, None)))
    }
    "translate CAST(a AS numeric)" in {
      exampleExpr("CAST(a AS numeric)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.DecimalType(None, None)))
    }
    "translate CAST(a AS binary)" in {
      exampleExpr("CAST(a AS binary)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.BinaryType))
    }
    "translate CAST(a AS varbinary)" in {
      exampleExpr("CAST(a AS varbinary)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.BinaryType))
    }
    "translate CAST(a AS json)" in {
      exampleExpr("CAST(a AS json)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.VarcharType(None)))
    }
    "translate CAST(a AS uniqueidentifier)" in {
      exampleExpr(
        "CAST(a AS uniqueidentifier)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = Some(16))))
    }

    "translate CAST pseudo function calls with length arguments" in {
      exampleExpr("CAST(a AS char(10))", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.CharType(size = Some(10))))
      exampleExpr(
        "CAST(a AS varchar(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = Some(10))))
      exampleExpr("CAST(a AS nchar(10))", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.CharType(size = Some(10))))
      exampleExpr(
        "CAST(a AS nvarchar(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = Some(10))))
    }

    "translate CAST pseudo function calls with scale arguments" in {
      exampleExpr(
        "CAST(a AS decimal(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), None)))
      exampleExpr(
        "CAST(a AS numeric(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), None)))
    }

    "translate CAST pseudo function calls with precision and scale arguments" in {
      exampleExpr(
        "CAST(a AS decimal(10, 2))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), Some(2))))
      exampleExpr(
        "CAST(a AS numeric(10, 2))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), Some(2))))
    }

    "translate TRY_CAST pseudo function calls with simple scalars" in {
      exampleExpr(
        "TRY_CAST(a AS tinyint)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.ByteType(size = Some(1)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS smallint)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.ShortType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS INT)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.IntegerType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS bigint)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.LongType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS bit)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.BooleanType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS money)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(19), Some(4)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS smallmoney)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), Some(4)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS float)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.FloatType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS real)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DoubleType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS date)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DateType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS time)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.TimeType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS datetime)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.TimestampType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS datetime2)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.TimestampType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS datetimeoffset)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.StringType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS smalldatetime)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.TimestampType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS char)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.CharType(size = None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS varchar)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS nchar)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.CharType(size = None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS nvarchar)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS text)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS ntext)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS image)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.BinaryType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS decimal)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(None, None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS numeric)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(None, None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS binary)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.BinaryType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS varbinary)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.BinaryType, returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS json)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS uniqueidentifier)",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = Some(16)), returnNullOnError = true))
    }

    "translate TRY_CAST pseudo function calls with length arguments" in {
      exampleExpr(
        "TRY_CAST(a AS char(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.CharType(size = Some(10)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS varchar(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = Some(10)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS nchar(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.CharType(size = Some(10)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS nvarchar(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.VarcharType(size = Some(10)), returnNullOnError = true))
    }

    "translate TRY_CAST pseudo function calls with scale arguments" in {
      exampleExpr(
        "TRY_CAST(a AS decimal(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), None), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS numeric(10))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), None), returnNullOnError = true))
    }

    "translate TRY_CAST pseudo function calls with precision and scale arguments" in {
      exampleExpr(
        "TRY_CAST(a AS decimal(10, 2))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), Some(2)), returnNullOnError = true))
      exampleExpr(
        "TRY_CAST(a AS numeric(10, 2))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.DecimalType(Some(10), Some(2)), returnNullOnError = true))
    }

    "translate identity to UnparsedType" in {
      // TODO: Resolve what to do with IDENTITY
      // IDENTITY it isn't actually castable but we have not implemented CREATE TABLE yet, so cover here for now
      // then examine what happens in snowflake
      exampleExpr(
        "CAST(a AS col1 IDENTITY(10, 2))",
        _.expression(),
        ir.Cast(simplyNamedColumn("a"), ir.UnparsedType("col1IDENTITY(10,2)")))
    }

    "translate unknown types to UnParsedType" in {
      exampleExpr("CAST(a AS sometype)", _.expression(), ir.Cast(simplyNamedColumn("a"), ir.UnparsedType("sometype")))
    }

  }
}
