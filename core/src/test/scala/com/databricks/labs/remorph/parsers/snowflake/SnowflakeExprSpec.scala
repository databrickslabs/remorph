package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.mockito.Mockito._
import org.scalatestplus.mockito.MockitoSugar
import scala.collection.JavaConverters._

class SnowflakeExprSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers with MockitoSugar {

  override protected def astBuilder: SnowflakeExpressionBuilder = new SnowflakeExpressionBuilder

  private def example(input: String, expectedAst: Expression): Assertion = example(input, _.expr(), expectedAst)

  "SnowflakeExpressionBuilder" should {
    "" in {
      example("d.s.sequence_1.NEXTVAL", NextValue("d.s.sequence_1"))
      example(
        "d.s.t.column_1[41 + 1]",
        ArrayAccess(Column("d.s.t.column_1"), Add(Literal(integer = Some(41)), Literal(integer = Some(1)))))
      example(
        "d.s.t.column_1:field_1.\"inner field\"",
        JsonAccess(Column("d.s.t.column_1"), Seq("field_1", "inner field")))
      example("d.s.t.column_1 COLLATE 'en_US-trim'", Collate(Column("d.s.t.column_1"), "en_US-trim"))
    }

    "translate unary arithmetic operators" in {
      example("+column_1", UPlus(Column("column_1")))
      example("+42", UPlus(Literal(integer = Some(42))))
      example("-column_1", UMinus(Column("column_1")))
      example("-42", UMinus(Literal(integer = Some(42))))
      example("NOT true", Not(Literal(boolean = Some(true))))
      example("NOT column_2", Not(Column("column_2")))
    }

    "translate binary arithmetic operators" in {
      example("1+1", Add(Literal(integer = Some(1)), Literal(integer = Some(1))))
      example("2 * column_1", Multiply(Literal(integer = Some(2)), Column("column_1")))
      example("column_1 - 1", Subtract(Column("column_1"), Literal(integer = Some(1))))
      example("column_1/column_2", Divide(Column("column_1"), Column("column_2")))
      example("42 % 2", Mod(Literal(integer = Some(42)), Literal(integer = Some(2))))
      example("'foo' || column_1", Concat(Literal(string = Some("foo")), Column("column_1")))
    }

    "translate IFF expression" in {
      example(
        "IFF (true, column_1, column_2)",
        Iff(Literal(boolean = Some(true)), Column("column_1"), Column("column_2")))
    }

    "translate array literals" in {
      example(
        "[1, 2, 3]",
        Literal(array = Some(
          ArrayExpr(None, Seq(Literal(integer = Some(1)), Literal(integer = Some(2)), Literal(integer = Some(3)))))))
      example("[1,column_1,2]", UnresolvedExpression("[1,column_1,2]"))
    }

    "translate cast expressions" in {
      example("CAST (column_1 AS BOOLEAN)", Cast(Column("column_1"), BooleanType()))
      example("TRY_CAST (column_1 AS BOOLEAN)", Cast(Column("column_1"), BooleanType(), returnNullOnError = true))
      example("TO_TIMESTAMP(1234567890)", Cast(Literal(integer = Some(1234567890)), TimestampNTZType()))
      example("TIME('00:00:00')", Cast(Literal(string = Some("00:00:00")), TimeType()))
      example("TO_TIME(column_1)", Cast(Column("column_1"), TimeType()))
      example("DATE(column_1)", Cast(Column("column_1"), DateType()))
      example("TO_DATE('2024-05-15')", Cast(Literal(string = Some("2024-05-15")), DateType()))
      example("INTERVAL '1 hour'", Cast(Literal(string = Some("1 hour")), IntervalType()))
      example("42::FLOAT", Cast(Literal(integer = Some(42)), DoubleType()))
    }
  }

  "SnowflakeExpressionBuilder.buildOp" should {
    "handle unresolved input" in {
      val exprContext = mock[ExprContext]
      val threeOperands = List.fill[ExprContext](3)(mock[ExprContext]).asJava
      when(exprContext.expr()).thenReturn(threeOperands)
      val dummyTextForExprContext = "dummy"
      when(exprContext.getText).thenReturn(dummyTextForExprContext)
      astBuilder.buildOp(exprContext) shouldBe UnresolvedExpression(dummyTextForExprContext)
      verify(exprContext).expr()
      verify(exprContext).getText
      verifyNoMoreInteractions(exprContext)
    }
  }
}
