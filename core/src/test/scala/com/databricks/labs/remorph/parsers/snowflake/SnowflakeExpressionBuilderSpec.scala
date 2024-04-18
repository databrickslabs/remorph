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

    "translate a query with a window function" in {

      example(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(Column("a"), DescendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))

      example(
        query = "ROW_NUMBER() OVER (PARTITION BY a)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(Column("a")),
          sort_order = Seq(),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))
      example(
        query = "NTILE(42) OVER (PARTITION BY a ORDER BY b, c DESC, d)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = NTile(Literal(integer = Some(42))),
          partition_spec = Seq(Column("a")),
          sort_order = Seq(
            SortOrder(Column("b"), AscendingSortDirection, SortNullsLast),
            SortOrder(Column("c"), DescendingSortDirection, SortNullsLast),
            SortOrder(Column("d"), AscendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))
    }

    "missing bits in window function grammar" ignore {

      // line 1:35 mismatched input 'NULLS' expecting {')', ','}
      example(
        query = "ROW_NUMBER() OVER (ORDER BY a DESC NULLS FIRST)",
        rule = _.ranking_windowed_function(),
        expectedAst = Window(
          window_function = RowNumber,
          partition_spec = Seq(),
          sort_order = Seq(SortOrder(Column("a"), DescendingSortDirection, SortNullsLast)),
          frame_spec = WindowFrame(
            frame_type = RowsFrame,
            lower = FrameBoundary(current_row = false, unbounded = true, value = Noop),
            upper = FrameBoundary(current_row = true, unbounded = false, value = Noop))))

      // line 1:33 no viable alternative at input 'a ROWS'
      example(
        query = "ROW_NUMBER() OVER(PARTITION BY a ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
        rule = _.ranking_windowed_function(),
        expectedAst = null)
    }
  }
}
