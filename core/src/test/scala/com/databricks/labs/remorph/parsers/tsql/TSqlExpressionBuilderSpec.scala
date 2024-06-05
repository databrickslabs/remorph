package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.FrameBoundary
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.WindowFrameBoundContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.antlr.v4.runtime.tree.TerminalNodeImpl
import org.antlr.v4.runtime.{CommonToken, Token}
import org.mockito.ArgumentMatchers.{any, anyInt}
import org.mockito.Mockito.{mock, when}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlExpressionBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlExpressionBuilder(new TSqlFunctionBuilder)

  "TSqlExpressionBuilder" should {
    "translate literals" in {
      example("null", _.expression(), ir.Literal(nullType = Some(ir.NullType())))
      example("1", _.expression(), ir.Literal(integer = Some(1)))
      example("-1", _.expression(), ir.Literal(integer = Some(-1)))
      example("+1", _.expression(), ir.Literal(integer = Some(1)))
      example("1.1", _.expression(), ir.Literal(float = Some(1.1f)))
      example("'foo'", _.expression(), ir.Literal(string = Some("foo")))
    }
    "translate scientific notation" in {
      example("1.1e2", _.expression(), ir.Literal(integer = Some(110)))
      example("1.1e-2", _.expression(), ir.Literal(float = Some(0.011f)))
      example("1e2", _.expression(), ir.Literal(integer = Some(100)))
      example("0.123456789", _.expression(), ir.Literal(double = Some(0.123456789)))
      example(
        "0.123456789e-1234",
        _.expression(),
        ir.Literal(decimal = Some(ir.Decimal("0.123456789e-1234", None, None))))
    }
    "translate simple numeric binary expressions" in {
      example("1 + 2", _.expression(), ir.Add(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 - 2", _.expression(), ir.Subtract(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 * 2", _.expression(), ir.Multiply(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 / 2", _.expression(), ir.Divide(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("1 % 2", _.expression(), ir.Mod(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))))
      example("'A' || 'B'", _.expression(), ir.Concat(ir.Literal(string = Some("A")), ir.Literal(string = Some("B"))))
      example("4 ^ 2", _.expression(), ir.BitwiseXor(ir.Literal(integer = Some(4)), ir.Literal(integer = Some(2))))
    }
    "translate complex binary expressions" in {
      example(
        "a + b * 2",
        _.expression(),
        ir.Add(ir.Column("a"), ir.Multiply(ir.Column("b"), ir.Literal(integer = Some(2)))))
      example(
        "(a + b) * 2",
        _.expression(),
        ir.Multiply(ir.Add(ir.Column("a"), ir.Column("b")), ir.Literal(integer = Some(2))))
      example("a & b | c", _.expression(), ir.BitwiseOr(ir.BitwiseAnd(ir.Column("a"), ir.Column("b")), ir.Column("c")))
      example(
        "(a & b) | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(ir.Column("a"), ir.Column("b")), ir.Column("c")))
      example(
        "a + b * 2",
        _.expression(),
        ir.Add(ir.Column("a"), ir.Multiply(ir.Column("b"), ir.Literal(integer = Some(2)))))
      example(
        "(a + b) * 2",
        _.expression(),
        ir.Multiply(ir.Add(ir.Column("a"), ir.Column("b")), ir.Literal(integer = Some(2))))
      example("a & b | c", _.expression(), ir.BitwiseOr(ir.BitwiseAnd(ir.Column("a"), ir.Column("b")), ir.Column("c")))
      example(
        "(a & b) | c",
        _.expression(),
        ir.BitwiseOr(ir.BitwiseAnd(ir.Column("a"), ir.Column("b")), ir.Column("c")))
      example(
        "a % 3 + b * 2 - c / 5",
        _.expression(),
        ir.Subtract(
          ir.Add(
            ir.Mod(ir.Column("a"), ir.Literal(integer = Some(3))),
            ir.Multiply(ir.Column("b"), ir.Literal(integer = Some(2)))),
          ir.Divide(ir.Column("c"), ir.Literal(integer = Some(5)))))
      example(
        query = "a || b || c",
        _.expression(),
        ir.Concat(ir.Concat(ir.Column("a"), ir.Column("b")), ir.Column("c")))
    }
    "correctly apply operator precedence and associativity" in {
      example(
        "1 + -++-2",
        _.expression(),
        ir.Add(ir.Literal(integer = Some(1)), ir.UMinus(ir.UPlus(ir.UPlus(ir.Literal(integer = Some(-2)))))))
      example(
        "1 + ~ 2 * 3",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(ir.BitwiseNot(ir.Literal(integer = Some(2))), ir.Literal(integer = Some(3)))))
      example(
        "1 + -2 * 3",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(ir.Literal(integer = Some(-2)), ir.Literal(integer = Some(3)))))
      example(
        "1 + -2 * 3 + 7 & 66",
        _.expression(),
        ir.BitwiseAnd(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.Literal(integer = Some(-2)), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 ^ 66",
        _.expression(),
        ir.BitwiseXor(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.Literal(integer = Some(-2)), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 | 66",
        _.expression(),
        ir.BitwiseOr(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.Literal(integer = Some(-2)), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.Literal(integer = Some(66))))
      example(
        "1 + -2 * 3 + 7 + ~66",
        _.expression(),
        ir.Add(
          ir.Add(
            ir.Add(
              ir.Literal(integer = Some(1)),
              ir.Multiply(ir.Literal(integer = Some(-2)), ir.Literal(integer = Some(3)))),
            ir.Literal(integer = Some(7))),
          ir.BitwiseNot(ir.Literal(integer = Some(66)))))
      example(
        "1 + -2 * 3 + 7 | 1980 || 'leeds1' || 'leeds2' || 'leeds3'",
        _.expression(),
        ir.Concat(
          ir.Concat(
            ir.Concat(
              ir.BitwiseOr(
                ir.Add(
                  ir.Add(
                    ir.Literal(integer = Some(1)),
                    ir.Multiply(ir.Literal(integer = Some(-2)), ir.Literal(integer = Some(3)))),
                  ir.Literal(integer = Some(7))),
                ir.Literal(integer = Some(1980))),
              ir.Literal(string = Some("leeds1"))),
            ir.Literal(string = Some("leeds2"))),
          ir.Literal(string = Some("leeds3"))))
    }
    "correctly respect explicit precedence with parentheses" in {
      example(
        "(1 + 2) * 3",
        _.expression(),
        ir.Multiply(
          ir.Add(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))),
          ir.Literal(integer = Some(3))))
      example(
        "1 + (2 * 3)",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3)))))
      example(
        "(1 + 2) * (3 + 4)",
        _.expression(),
        ir.Multiply(
          ir.Add(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(2))),
          ir.Add(ir.Literal(integer = Some(3)), ir.Literal(integer = Some(4)))))
      example(
        "1 + (2 * 3) + 4",
        _.expression(),
        ir.Add(
          ir.Add(
            ir.Literal(integer = Some(1)),
            ir.Multiply(ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3)))),
          ir.Literal(integer = Some(4))))
      example(
        "1 + (2 * 3 + 4)",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Add(
            ir.Multiply(ir.Literal(integer = Some(2)), ir.Literal(integer = Some(3))),
            ir.Literal(integer = Some(4)))))
      example(
        "1 + (2 * (3 + 4))",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(
            ir.Literal(integer = Some(2)),
            ir.Add(ir.Literal(integer = Some(3)), ir.Literal(integer = Some(4))))))
      example(
        "(1 + (2 * (3 + 4)))",
        _.expression(),
        ir.Add(
          ir.Literal(integer = Some(1)),
          ir.Multiply(
            ir.Literal(integer = Some(2)),
            ir.Add(ir.Literal(integer = Some(3)), ir.Literal(integer = Some(4))))))
    }

    "correctly resolve dot delimited plain references" in {
      example("a", _.expression(), ir.Column("a"))
      example("a.b", _.expression(), ir.Column("a.b"))
      example("a.b.c", _.expression(), ir.Column("a.b.c"))
    }

    "correctly resolve quoted identifiers" in {
      example("RAW", _.expression(), ir.Column("RAW"))
      example("#RAW", _.expression(), ir.Column("#RAW"))
      example("\"a\"", _.expression(), ir.Column("\"a\""))
      example("[a]", _.expression(), ir.Column("[a]"))
      example("[a].[b]", _.expression(), ir.Column("[a].[b]"))
      example("[a].[b].[c]", _.expression(), ir.Column("[a].[b].[c]"))
    }

    "correctly resolve keywords used as identifiers" in {
      example("ABORT", _.expression(), ir.Column("ABORT"))
    }

    "translate a simple column" in {
      example("a", _.selectListElem(), ir.Column("a"))
      example("#a", _.selectListElem(), ir.Column("#a"))
      example("[a]", _.selectListElem(), ir.Column("[a]"))
      example("\"a\"", _.selectListElem(), ir.Column("\"a\""))
      example("RAW", _.selectListElem(), ir.Column("RAW"))
    }

    "translate a column with a table" in {
      example("table_x.a", _.selectListElem(), ir.Column("table_x.a"))
    }

    "translate a column with a schema" in {
      example("schema1.table_x.a", _.selectListElem(), ir.Column("schema1.table_x.a"))
    }

    "translate a column with a database" in {
      example("database1.schema1.table_x.a", _.selectListElem(), ir.Column("database1.schema1.table_x.a"))
    }

    "translate a column with a server" in {
      example("server1..schema1.table_x.a", _.fullColumnName(), ir.Column("server1..schema1.table_x.a"))
    }

    "translate a column without a table reference" in {
      example("a", _.fullColumnName(), ir.Column("a"))
    }

    "return ir.Dot for otherwise unhandled DotExpr" in {
      val builder = new TSqlExpressionBuilder(new TSqlFunctionBuilder)
      val mockDotExprCtx = mock(classOf[TSqlParser.ExprDotContext])
      val mockExpressionCtx = mock(classOf[TSqlParser.ExpressionContext])
      val mockVisitor = mock(classOf[TSqlExpressionBuilder])

      when(mockDotExprCtx.expression(anyInt())).thenReturn(mockExpressionCtx)
      when(mockExpressionCtx.accept(mockVisitor)).thenReturn(ir.Literal(string = Some("a")))
      val result = builder.visitExprDot(mockDotExprCtx)

      result shouldBe a[ir.Dot]
    }

    "cover the unreachable default case in buildFrame" in {
      val mockCtx = mock(classOf[WindowFrameBoundContext])

      // Ensure that UNBOUNDED(), CURRENT() and INT() methods return null
      when(mockCtx.UNBOUNDED()).thenReturn(null)
      when(mockCtx.CURRENT()).thenReturn(null)
      when(mockCtx.INT()).thenReturn(null)

      val builder = new TSqlExpressionBuilder(new TSqlFunctionBuilder)
      val result = builder.buildFrame(mockCtx)

      // Verify the result
      result shouldBe a[FrameBoundary]
      result.current_row shouldBe false
      result.unbounded shouldBe false
    }

    "translate search conditions" in {
      example("a = b", _.searchCondition(), ir.Equals(ir.Column("a"), ir.Column("b")))
      example("a > b", _.searchCondition(), ir.GreaterThan(ir.Column("a"), ir.Column("b")))
      example("a < b", _.searchCondition(), ir.LesserThan(ir.Column("a"), ir.Column("b")))
      example("a >= b", _.searchCondition(), ir.GreaterThanOrEqual(ir.Column("a"), ir.Column("b")))
      example("a <= b", _.searchCondition(), ir.LesserThanOrEqual(ir.Column("a"), ir.Column("b")))
      example("a > = b", _.searchCondition(), ir.GreaterThanOrEqual(ir.Column("a"), ir.Column("b")))
      example("a <  = b", _.searchCondition(), ir.LesserThanOrEqual(ir.Column("a"), ir.Column("b")))
      example("a <> b", _.searchCondition(), ir.NotEquals(ir.Column("a"), ir.Column("b")))
      example("NOT a = b", _.searchCondition(), ir.Not(ir.Equals(ir.Column("a"), ir.Column("b"))))
      example(
        "a = b AND c = e",
        _.searchCondition(),
        ir.And(ir.Equals(ir.Column("a"), ir.Column("b")), ir.Equals(ir.Column("c"), ir.Column("e"))))
      example(
        "a = b OR c = e",
        _.searchCondition(),
        ir.Or(ir.Equals(ir.Column("a"), ir.Column("b")), ir.Equals(ir.Column("c"), ir.Column("e"))))
      example(
        "a = b AND c = x OR e = f",
        _.searchCondition(),
        ir.Or(
          ir.And(ir.Equals(ir.Column("a"), ir.Column("b")), ir.Equals(ir.Column("c"), ir.Column("x"))),
          ir.Equals(ir.Column("e"), ir.Column("f"))))
      example(
        "a = b AND (c = x OR e = f)",
        _.searchCondition(),
        ir.And(
          ir.Equals(ir.Column("a"), ir.Column("b")),
          ir.Or(ir.Equals(ir.Column("c"), ir.Column("x")), ir.Equals(ir.Column("e"), ir.Column("f")))))
    }

    "handle non special functions used in dot operators" in {
      example(
        "a.b()",
        _.expression(),
        ir.Dot(
          ir.Column("a"),
          ir.UnresolvedFunction("b", List(), is_distinct = false, is_user_defined_function = false)))
      example(
        "a.b.c()",
        _.expression(),
        ir.Dot(
          ir.Column("a"),
          ir.Dot(
            ir.Column("b"),
            ir.UnresolvedFunction("c", List(), is_distinct = false, is_user_defined_function = false))))
      example(
        "a.b.c.FLOOR(c)",
        _.expression(),
        ir.Dot(
          ir.Column("a"),
          ir.Dot(ir.Column("b"), ir.Dot(ir.Column("c"), ir.CallFunction("FLOOR", Seq(ir.Column("c")))))))
    }

    "handle unknown functions used with dots" in {
      example(
        "a.UNKNOWN_FUNCTION()",
        _.expression(),
        ir.Dot(
          ir.Column("a"),
          ir.UnresolvedFunction("UNKNOWN_FUNCTION", List(), is_distinct = false, is_user_defined_function = false)))
    }

    "cover case that cannot happen with dot" in {
      val builder = new TSqlExpressionBuilder(new TSqlFunctionBuilder)

      val mockCtx = mock(classOf[TSqlParser.ExprDotContext])
      val expressionMockColumn = mock(classOf[TSqlParser.ExpressionContext])
      when(mockCtx.expression(0)).thenReturn(expressionMockColumn)
      when(expressionMockColumn.accept(any())).thenReturn(ir.Column("a"))
      val expressionMockFunc = mock(classOf[TSqlParser.ExpressionContext])
      when(mockCtx.expression(1)).thenReturn(expressionMockFunc)
      when(expressionMockFunc.accept(any())).thenReturn(ir.CallFunction("UNKNOWN_FUNCTION", List()))
      val result = builder.visitExprDot(mockCtx)
      result shouldBe a[ir.Dot]
    }

    "translate case/when/else expressions" in {
      // Case with an initial expression and an else clause
      example(
        "CASE a WHEN 1 THEN 'one' WHEN 2 THEN 'two' ELSE 'other' END",
        _.expression(),
        ir.Case(
          Some(ir.Column("a")),
          Seq(
            ir.WhenBranch(ir.Literal(integer = Some(1)), ir.Literal(string = Some("one"))),
            ir.WhenBranch(ir.Literal(integer = Some(2)), ir.Literal(string = Some("two")))),
          Some(ir.Literal(string = Some("other")))))

      // Case without an initial expression and with an else clause
      example(
        "CASE WHEN a = 1 THEN 'one' WHEN a = 2 THEN 'two' ELSE 'other' END",
        _.expression(),
        ir.Case(
          None,
          Seq(
            ir.WhenBranch(ir.Equals(ir.Column("a"), ir.Literal(integer = Some(1))), ir.Literal(string = Some("one"))),
            ir.WhenBranch(ir.Equals(ir.Column("a"), ir.Literal(integer = Some(2))), ir.Literal(string = Some("two")))),
          Some(ir.Literal(string = Some("other")))))

      // Case with an initial expression and without an else clause
      example(
        "CASE a WHEN 1 THEN 'one' WHEN 2 THEN 'two' END",
        _.expression(),
        ir.Case(
          Some(ir.Column("a")),
          Seq(
            ir.WhenBranch(ir.Literal(integer = Some(1)), ir.Literal(string = Some("one"))),
            ir.WhenBranch(ir.Literal(integer = Some(2)), ir.Literal(string = Some("two")))),
          None))

      // Case without an initial expression and without an else clause
      example(
        "CASE WHEN a = 1 AND b < 7 THEN 'one' WHEN a = 2 THEN 'two' END",
        _.expression(),
        ir.Case(
          None,
          Seq(
            ir.WhenBranch(
              ir.And(
                ir.Equals(ir.Column("a"), ir.Literal(integer = Some(1))),
                ir.LesserThan(ir.Column("b"), ir.Literal(integer = Some(7)))),
              ir.Literal(string = Some("one"))),
            ir.WhenBranch(ir.Equals(ir.Column("a"), ir.Literal(integer = Some(2))), ir.Literal(string = Some("two")))),
          None))
    }

    "translate the $ACTION special column reference" in {
      example("$ACTION", _.expression(), ir.DollarAction())
    }

    "translate a timezone reference" in {
      example("a AT TIME ZONE 'UTC'", _.expression(), ir.Timezone(ir.Column("a"), ir.Literal(string = Some("UTC"))))
    }

    "return UnresolvedExpression for unsupported SelectListElem" in {
      val builder = new TSqlExpressionBuilder(new TSqlFunctionBuilder)

      val mockCtx = mock(classOf[TSqlParser.SelectListElemContext])

      // Ensure that both asterisk() and expressionElem() methods return null
      when(mockCtx.asterisk()).thenReturn(null)
      when(mockCtx.expressionElem()).thenReturn(null)

      // Call the method with the mock instance
      val result = builder.visitSelectListElem(mockCtx)

      // Verify the result
      result shouldBe a[ir.UnresolvedExpression]
    }

    "cover default case in buildLocalAssign via visitSelectListElem" in {
      val selectListElemContextMock = mock(classOf[TSqlParser.SelectListElemContext])
      val eofToken = new CommonToken(Token.EOF)
      selectListElemContextMock.op = eofToken
      when(selectListElemContextMock.LOCAL_ID()).thenReturn(new TerminalNodeImpl(eofToken))
      when(selectListElemContextMock.asterisk()).thenReturn(null)
      when(selectListElemContextMock.udtElem()).thenReturn(null)
      when(selectListElemContextMock.getText).thenReturn("")

      val expressionContextMock = mock(classOf[TSqlParser.ExpressionContext])
      when(expressionContextMock.accept(any())).thenReturn(null)
      when(selectListElemContextMock.expression()).thenReturn(expressionContextMock)

      val builder = new TSqlExpressionBuilder(new TSqlFunctionBuilder)
      val result = builder.visitSelectListElem(selectListElemContextMock)

      result shouldBe a[ir.UnresolvedExpression]
    }

    "translate CAST pseudo function calls with simple scalars" in {
      example("CAST(a AS tinyint)", _.expression(), ir.Cast(ir.Column("a"), ir.ByteType(size = Some(1))))
      example("CAST(a AS smallint)", _.expression(), ir.Cast(ir.Column("a"), ir.ShortType()))
      example("CAST(a AS INT)", _.expression(), ir.Cast(ir.Column("a"), ir.IntegerType()))
      example("CAST(a AS bigint)", _.expression(), ir.Cast(ir.Column("a"), ir.LongType()))
      example("CAST(a AS bit)", _.expression(), ir.Cast(ir.Column("a"), ir.BooleanType()))
      example("CAST(a AS money)", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(Some(19), Some(4))))
      example("CAST(a AS smallmoney)", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), Some(4))))
      example("CAST(a AS float)", _.expression(), ir.Cast(ir.Column("a"), ir.FloatType()))
      example("CAST(a AS real)", _.expression(), ir.Cast(ir.Column("a"), ir.DoubleType()))
      example("CAST(a AS date)", _.expression(), ir.Cast(ir.Column("a"), ir.DateType()))
      example("CAST(a AS time)", _.expression(), ir.Cast(ir.Column("a"), ir.TimeType()))
      example("CAST(a AS datetime)", _.expression(), ir.Cast(ir.Column("a"), ir.TimestampType()))
      example("CAST(a AS datetime2)", _.expression(), ir.Cast(ir.Column("a"), ir.TimestampType()))
      example("CAST(a AS datetimeoffset)", _.expression(), ir.Cast(ir.Column("a"), ir.StringType()))
      example("CAST(a AS smalldatetime)", _.expression(), ir.Cast(ir.Column("a"), ir.TimestampType()))
      example("CAST(a AS char)", _.expression(), ir.Cast(ir.Column("a"), ir.CharType(size = None)))
      example("CAST(a AS varchar)", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(size = None)))
      example("CAST(a AS nchar)", _.expression(), ir.Cast(ir.Column("a"), ir.CharType(size = None)))
      example("CAST(a AS nvarchar)", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(size = None)))
      example("CAST(a AS text)", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(None)))
      example("CAST(a AS ntext)", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(None)))
      example("CAST(a AS image)", _.expression(), ir.Cast(ir.Column("a"), ir.BinaryType()))
      example("CAST(a AS decimal)", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(None, None)))
      example("CAST(a AS numeric)", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(None, None)))
      example("CAST(a AS binary)", _.expression(), ir.Cast(ir.Column("a"), ir.BinaryType()))
      example("CAST(a AS varbinary)", _.expression(), ir.Cast(ir.Column("a"), ir.BinaryType()))
      example("CAST(a AS json)", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(None)))
      example("CAST(a AS uniqueidentifier)", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(size = Some(16))))
    }

    "translate CAST pseudo function calls with length arguments" in {
      example("CAST(a AS char(10))", _.expression(), ir.Cast(ir.Column("a"), ir.CharType(size = Some(10))))
      example("CAST(a AS varchar(10))", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(size = Some(10))))
      example("CAST(a AS nchar(10))", _.expression(), ir.Cast(ir.Column("a"), ir.CharType(size = Some(10))))
      example("CAST(a AS nvarchar(10))", _.expression(), ir.Cast(ir.Column("a"), ir.VarCharType(size = Some(10))))
    }

    "translate CAST pseudo function calls with scale arguments" in {
      example("CAST(a AS decimal(10))", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), None)))
      example("CAST(a AS numeric(10))", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), None)))
    }

    "translate CAST pseudo function calls with precision and scale arguments" in {
      example("CAST(a AS decimal(10, 2))", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), Some(2))))
      example("CAST(a AS numeric(10, 2))", _.expression(), ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), Some(2))))
    }

    "translate TRY_CAST pseudo function calls with simple scalars" in {
      example(
        "TRY_CAST(a AS tinyint)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.ByteType(size = Some(1)), returnNullOnError = true))
      example(
        "TRY_CAST(a AS smallint)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.ShortType(), returnNullOnError = true))
      example("TRY_CAST(a AS INT)", _.expression(), ir.Cast(ir.Column("a"), ir.IntegerType(), returnNullOnError = true))
      example("TRY_CAST(a AS bigint)", _.expression(), ir.Cast(ir.Column("a"), ir.LongType(), returnNullOnError = true))
      example("TRY_CAST(a AS bit)", _.expression(), ir.Cast(ir.Column("a"), ir.BooleanType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS money)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(Some(19), Some(4)), returnNullOnError = true))
      example(
        "TRY_CAST(a AS smallmoney)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), Some(4)), returnNullOnError = true))
      example("TRY_CAST(a AS float)", _.expression(), ir.Cast(ir.Column("a"), ir.FloatType(), returnNullOnError = true))
      example("TRY_CAST(a AS real)", _.expression(), ir.Cast(ir.Column("a"), ir.DoubleType(), returnNullOnError = true))
      example("TRY_CAST(a AS date)", _.expression(), ir.Cast(ir.Column("a"), ir.DateType(), returnNullOnError = true))
      example("TRY_CAST(a AS time)", _.expression(), ir.Cast(ir.Column("a"), ir.TimeType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS datetime)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.TimestampType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS datetime2)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.TimestampType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS datetimeoffset)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.StringType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS smalldatetime)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.TimestampType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS char)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.CharType(size = None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS varchar)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(size = None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS nchar)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.CharType(size = None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS nvarchar)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(size = None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS text)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS ntext)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS image)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.BinaryType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS decimal)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(None, None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS numeric)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(None, None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS binary)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.BinaryType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS varbinary)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.BinaryType(), returnNullOnError = true))
      example(
        "TRY_CAST(a AS json)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS uniqueidentifier)",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(size = Some(16)), returnNullOnError = true))
    }

    "translate TRY_CAST pseudo function calls with length arguments" in {
      example(
        "TRY_CAST(a AS char(10))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.CharType(size = Some(10)), returnNullOnError = true))
      example(
        "TRY_CAST(a AS varchar(10))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(size = Some(10)), returnNullOnError = true))
      example(
        "TRY_CAST(a AS nchar(10))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.CharType(size = Some(10)), returnNullOnError = true))
      example(
        "TRY_CAST(a AS nvarchar(10))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.VarCharType(size = Some(10)), returnNullOnError = true))
    }

    "translate TRY_CAST pseudo function calls with scale arguments" in {
      example(
        "TRY_CAST(a AS decimal(10))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), None), returnNullOnError = true))
      example(
        "TRY_CAST(a AS numeric(10))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), None), returnNullOnError = true))
    }

    "translate TRY_CAST pseudo function calls with precision and scale arguments" in {
      example(
        "TRY_CAST(a AS decimal(10, 2))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), Some(2)), returnNullOnError = true))
      example(
        "TRY_CAST(a AS numeric(10, 2))",
        _.expression(),
        ir.Cast(ir.Column("a"), ir.DecimalType(Some(10), Some(2)), returnNullOnError = true))
    }

    "translate identity to UnparsedType" in {
      // TODO: Resolve what to do with IDENTITY
      // IDENTITY it isn't actually castable but we have not implemented CREATE TABLE yet, so cover here for now
      // then examine what happens in snowflake
      example("CAST(a AS col1 IDENTITY(10, 2))", _.expression(), ir.Cast(ir.Column("a"), ir.UnparsedType()))
    }

    "translate unknown types to UnParsedType" in {
      example("CAST(a AS sometype)", _.expression(), ir.Cast(ir.Column("a"), ir.UnparsedType()))
    }
  }
}
