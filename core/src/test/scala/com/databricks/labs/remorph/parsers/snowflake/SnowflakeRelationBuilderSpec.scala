package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{Builtin_functionContext, Id_Context, Join_typeContext, Outer_joinContext}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.mockito.Mockito._
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeRelationBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers with MockitoSugar {

  override protected def astBuilder: SnowflakeRelationBuilder = new SnowflakeRelationBuilder

  "SnowflakeRelationBuilder" should {

    "translate FROM clauses" in {
      example("FROM some_table", _.from_clause(), namedTable("some_table"))
    }

    "translate WHERE clauses" in {
      example(
        "FROM some_table WHERE 1=1",
        _.select_optional_clauses(),
        Filter(namedTable("some_table"), Equals(Literal(integer = Some(1)), Literal(integer = Some(1)))))
    }

    "translate GROUP BY clauses" in {
      example(
        "FROM some_table GROUP BY some_column",
        _.select_optional_clauses(),
        Aggregate(
          input = namedTable("some_table"),
          group_type = GroupBy,
          grouping_expressions = Seq(Column("some_column")),
          pivot = None))

      example(
        query = "FROM t1 PIVOT (AVG(a) FOR d IN('x', 'y'))",
        rule = _.select_optional_clauses(),
        Aggregate(
          input = namedTable("t1"),
          group_type = Pivot,
          grouping_expressions = Seq(Avg(Column("a"))),
          pivot = Some(Pivot(Column("d"), Seq(Literal(string = Some("x")), Literal(string = Some("y")))))))

      example(
        query = "FROM t1 PIVOT (COUNT(a) FOR d IN('x', 'y'))",
        rule = _.select_optional_clauses(),
        Aggregate(
          input = namedTable("t1"),
          group_type = Pivot,
          grouping_expressions = Seq(Count(Column("a"))),
          pivot = Some(Pivot(Column("d"), Seq(Literal(string = Some("x")), Literal(string = Some("y")))))))

      example(
        query = "FROM t1 PIVOT (MIN(a) FOR d IN('x', 'y'))",
        rule = _.select_optional_clauses(),
        Aggregate(
          input = namedTable("t1"),
          group_type = Pivot,
          grouping_expressions = Seq(Min(Column("a"))),
          pivot = Some(Pivot(Column("d"), Seq(Literal(string = Some("x")), Literal(string = Some("y")))))))
    }

    "translate ORDER BY clauses" in {
      example(
        "FROM some_table ORDER BY some_column",
        _.select_optional_clauses(),
        Sort(
          namedTable("some_table"),
          Seq(SortOrder(Column("some_column"), AscendingSortDirection, SortNullsLast)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column ASC",
        _.select_optional_clauses(),
        Sort(
          namedTable("some_table"),
          Seq(SortOrder(Column("some_column"), AscendingSortDirection, SortNullsLast)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column ASC NULLS LAST",
        _.select_optional_clauses(),
        Sort(
          namedTable("some_table"),
          Seq(SortOrder(Column("some_column"), AscendingSortDirection, SortNullsLast)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC",
        _.select_optional_clauses(),
        Sort(
          namedTable("some_table"),
          Seq(SortOrder(Column("some_column"), DescendingSortDirection, SortNullsLast)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC NULLS LAST",
        _.select_optional_clauses(),
        Sort(
          namedTable("some_table"),
          Seq(SortOrder(Column("some_column"), DescendingSortDirection, SortNullsLast)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC NULLS FIRST",
        _.select_optional_clauses(),
        Sort(
          namedTable("some_table"),
          Seq(SortOrder(Column("some_column"), DescendingSortDirection, SortNullsFirst)),
          is_global = false))

    }

    "translate combinations of the above" in {
      example(
        "FROM some_table WHERE 1=1 GROUP BY some_column",
        _.select_optional_clauses(),
        Aggregate(
          input = Filter(namedTable("some_table"), Equals(Literal(integer = Some(1)), Literal(integer = Some(1)))),
          group_type = GroupBy,
          grouping_expressions = Seq(Column("some_column")),
          pivot = None))

      example(
        "FROM some_table WHERE 1=1 GROUP BY some_column ORDER BY some_column NULLS FIRST",
        _.select_optional_clauses(),
        Sort(
          Aggregate(
            input = Filter(namedTable("some_table"), Equals(Literal(integer = Some(1)), Literal(integer = Some(1)))),
            group_type = GroupBy,
            grouping_expressions = Seq(Column("some_column")),
            pivot = None),
          Seq(SortOrder(Column("some_column"), AscendingSortDirection, SortNullsFirst)),
          is_global = false))

      example(
        "FROM some_table WHERE 1=1 ORDER BY some_column NULLS FIRST",
        _.select_optional_clauses(),
        Sort(
          Filter(namedTable("some_table"), Equals(Literal(integer = Some(1)), Literal(integer = Some(1)))),
          Seq(SortOrder(Column("some_column"), AscendingSortDirection, SortNullsFirst)),
          is_global = false))
    }

    "translate CTE definitions" in {
      example(
        "WITH a (b, c) AS (SELECT x, y FROM d)",
        _.with_expression(),
        CTEDefinition("a", Seq(Column("b"), Column("c")), Project(namedTable("d"), Seq(Column("x"), Column("y")))))
    }

    "translate QUALIFY clauses" in {
      example(
        "FROM qt QUALIFY ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) = 1",
        _.select_optional_clauses(),
        Filter(
          input = namedTable("qt"),
          condition = Equals(
            Window(
              window_function = RowNumber,
              partition_spec = Seq(Column("p")),
              sort_order = Seq(SortOrder(Column("o"), AscendingSortDirection, SortNullsLast)),
              frame_spec = DummyWindowFrame),
            Literal(integer = Some(1)))))
    }

    "translate SELECT DISTINCT clauses" in {
      example(
        "SELECT DISTINCT a, b AS bb FROM t",
        _.select_statement(),
        Project(
          Deduplicate(
            input = namedTable("t"),
            column_names = Seq("a", "bb"),
            all_columns_as_keys = false,
            within_watermark = false),
          Seq(Column("a"), Alias(Column("b"), Seq("bb"), None))))

    }

    "translate SELECT TOP clauses" in {
      example("SELECT TOP 42 a FROM t", _.select_statement(), Project(Limit(namedTable("t"), 42), Seq(Column("a"))))

      example(
        "SELECT DISTINCT TOP 42 a FROM t",
        _.select_statement(),
        Project(
          Limit(Deduplicate(namedTable("t"), Seq("a"), all_columns_as_keys = false, within_watermark = false), 42),
          Seq(Column("a"))))
    }
  }

  "Unparsed input" should {
    "be reported as UnresolvedRelation" in {
      example("MATCH_RECOGNIZE()", _.match_recognize(), UnresolvedRelation("MATCH_RECOGNIZE()"))
    }
  }

  "SnowflakeRelationBuilder.translateJoinType" should {
    "handle unresolved join type" in {
      val outerJoin = mock[Outer_joinContext]
      val joinType = mock[Join_typeContext]
      when(joinType.outer_join()).thenReturn(outerJoin)
      astBuilder.translateJoinType(joinType) shouldBe UnspecifiedJoin
      verify(outerJoin).LEFT()
      verify(outerJoin).RIGHT()
      verify(outerJoin).FULL()
      verify(joinType, times(4)).outer_join()
    }
  }

  "SnowflakeRelationBuilder.translateAggregateFunction" should {
    "handler unresolved input" in {
      val param = parseString("x", _.id_())
      val builtinFunc = mock[Builtin_functionContext]
      val aggFunc = mock[Id_Context]
      when(aggFunc.builtin_function()).thenReturn(builtinFunc)
      val dummyTextForAggFunc = "dummy"
      when(aggFunc.getText).thenReturn(dummyTextForAggFunc)
      astBuilder.translateAggregateFunction(aggFunc, param) shouldBe UnresolvedExpression(dummyTextForAggFunc)
      verify(aggFunc, times(8)).builtin_function()
      verify(aggFunc).getText
      verifyNoMoreInteractions(aggFunc)
      verify(builtinFunc).AVG()
      verify(builtinFunc).SUM()
      verify(builtinFunc).COUNT()
      verify(builtinFunc).MIN()
      verifyNoMoreInteractions(builtinFunc)
    }
  }
}
