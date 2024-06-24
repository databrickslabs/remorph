package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IRHelpers, intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class TSqlRelationBuilderSpec
    extends AnyWordSpec
    with TSqlParserTestCommon
    with Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: TSqlRelationBuilder = new TSqlRelationBuilder

  "TSqlRelationBuilder" should {

    "translate query with no FROM clause" in {
      example("", _.selectOptionalClauses(), ir.NoTable())
    }

    "translate FROM clauses" in {
      example("FROM some_table", _.fromClause(), namedTable("some_table"))
      example("FROM some_schema.some_table", _.fromClause(), namedTable("some_schema.some_table"))
      example("FROM some_server..some_table", _.fromClause(), namedTable("some_server..some_table"))

      example(
        "FROM t1, t2, t3",
        _.fromClause(),
        ir.Join(
          ir.Join(
            namedTable("t1"),
            namedTable("t2"),
            None,
            ir.CrossJoin,
            Seq(),
            ir.JoinDataType(is_left_struct = false, is_right_struct = false)),
          namedTable("t3"),
          None,
          ir.CrossJoin,
          Seq(),
          ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }

    "translate WHERE clauses" in {
      example(
        "FROM some_table WHERE 1=1",
        _.selectOptionalClauses(),
        ir.Filter(namedTable("some_table"), ir.Equals(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(1)))))
    }

    "translate GROUP BY clauses" in {
      example(
        "FROM some_table GROUP BY some_column",
        _.selectOptionalClauses(),
        ir.Aggregate(
          input = namedTable("some_table"),
          group_type = ir.GroupBy,
          grouping_expressions = Seq(simplyNamedColumn("some_column")),
          pivot = None))

    }

    "translate ORDER BY clauses" in {
      example(
        "FROM some_table ORDER BY some_column",
        _.selectOptionalClauses(),
        ir.Sort(
          namedTable("some_table"),
          Seq(ir.SortOrder(simplyNamedColumn("some_column"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column ASC",
        _.selectOptionalClauses(),
        ir.Sort(
          namedTable("some_table"),
          Seq(ir.SortOrder(simplyNamedColumn("some_column"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
          is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC",
        _.selectOptionalClauses(),
        ir.Sort(
          namedTable("some_table"),
          Seq(ir.SortOrder(simplyNamedColumn("some_column"), ir.DescendingSortDirection, ir.SortNullsUnspecified)),
          is_global = false))
    }

    "translate combinations of the above" in {
      example(
        "FROM some_table WHERE 1=1 GROUP BY some_column",
        _.selectOptionalClauses(),
        ir.Aggregate(
          input = ir.Filter(
            namedTable("some_table"),
            ir.Equals(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(1)))),
          group_type = ir.GroupBy,
          grouping_expressions = Seq(simplyNamedColumn("some_column")),
          pivot = None))

      example(
        "FROM some_table WHERE 1=1 GROUP BY some_column ORDER BY some_column",
        _.selectOptionalClauses(),
        ir.Sort(
          ir.Aggregate(
            input = ir.Filter(
              namedTable("some_table"),
              ir.Equals(ir.Literal(integer = Some(1)), ir.Literal(integer = Some(1)))),
            group_type = ir.GroupBy,
            grouping_expressions = Seq(simplyNamedColumn("some_column")),
            pivot = None),
          Seq(ir.SortOrder(simplyNamedColumn("some_column"), ir.AscendingSortDirection, ir.SortNullsUnspecified)),
          is_global = false))

    }

    "translate CTE definitions" in {
      example(
        "WITH a (b, c) AS (SELECT x, y FROM d)",
        _.withExpression(),
        ir.CTEDefinition(
          "a",
          Seq(simplyNamedColumn("b"), simplyNamedColumn("c")),
          ir.Project(namedTable("d"), Seq(simplyNamedColumn("x"), simplyNamedColumn("y")))))
    }

    "translate SELECT DISTINCT clauses" in {
      example(
        "SELECT DISTINCT a, b AS bb FROM t",
        _.selectStatement(),
        ir.Project(
          ir.Deduplicate(
            input = namedTable("t"),
            column_names = Seq(ir.Id("a"), ir.Id("bb")),
            all_columns_as_keys = false,
            within_watermark = false),
          Seq(simplyNamedColumn("a"), ir.Alias(simplyNamedColumn("b"), Seq(ir.Id("bb")), None))))
    }
  }
}
