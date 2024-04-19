package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeRelationBuilderSpec extends AnyWordSpec with ParserTestCommon with Matchers {

  override def astBuilder: SnowflakeParserBaseVisitor[_] = new SnowflakeRelationBuilder

  private def namedTable(name: String): Relation = NamedTable(name, Map.empty, is_streaming = false)

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
  }
}
