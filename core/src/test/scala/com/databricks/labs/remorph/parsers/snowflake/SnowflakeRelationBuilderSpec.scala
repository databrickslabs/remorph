package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeRelationBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with Matchers {

  override protected def astBuilder: SnowflakeParserBaseVisitor[_] = new SnowflakeRelationBuilder

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
        "SELECT DISTINCT a FROM t",
        _.select_statement(),
        Project(
          Deduplicate(
            input = namedTable("t"),
            column_names = Seq("a"),
            all_columns_as_keys = false,
            within_watermark = false),
          Seq(Column("a"))))
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
}
