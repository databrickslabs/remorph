package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeExpressionBuilderSpec extends AnyWordSpec with ParserTestCommon with Matchers {

  override def astBuilder: SnowflakeParserBaseVisitor[_] = new SnowflakeExpressionBuilder

  "SnowflakeExpressionBuilder" should {
    "translate literals" in {
      example("null", _.literal(), Literal(nullType = Some(NullType())))
      example("true", _.literal(), Literal(boolean = Some(true)))
      example("false", _.literal(), Literal(boolean = Some(false)))
      example("1", _.literal(), Literal(integer = Some(1)))
      example("-1", _.literal(), Literal(integer = Some(-1)))
      example("1.1", _.literal(), Literal(float = Some(1.1f)))
      example("1.1e2", _.literal(), Literal(integer = Some(110)))
      example("1.1e-2", _.literal(), Literal(float = Some(0.011f)))
      example("0.123456789", _.literal(), Literal(double = Some(0.123456789)))
      example("0.123456789e-1234", _.literal(), Literal(decimal = Some(Decimal("0.123456789e-1234", None, None))))
      example("'foo'", _.literal(), Literal(string = Some("foo")))
    }

    "translate column names" in {
      example("x", _.column_name(), Column("x"))
    }

    "translate aggregation functions" in {
      example("COUNT(x)", _.aggregate_function(), Count(Column("x")))
    }
  }
}
