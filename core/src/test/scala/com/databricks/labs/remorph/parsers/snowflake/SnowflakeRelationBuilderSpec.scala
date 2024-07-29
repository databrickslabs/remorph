package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{JoinTypeContext, OuterJoinContext}
import org.antlr.v4.runtime.RuleContext
import org.mockito.Mockito._
import org.scalatest.Assertion
import org.scalatest.Checkpoints.Checkpoint
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeRelationBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: SnowflakeRelationBuilder = new SnowflakeRelationBuilder

  private def examples[R <: RuleContext](
      queries: Seq[String],
      rule: SnowflakeParser => R,
      expectedAst: LogicalPlan): Assertion = {
    val cp = new Checkpoint()
    queries.foreach(q => cp(example(q, rule, expectedAst)))
    cp.reportAll()
    succeed
  }

  "SnowflakeRelationBuilder" should {

    "translate query with no FROM clause" in {
      example("", _.selectOptionalClauses(), NoTable())
    }

    "translate FROM clauses" in {
      example("FROM some_table", _.fromClause(), namedTable("some_table"))
      example(
        "FROM t1, t2, t3",
        _.fromClause(),
        Join(
          Join(
            namedTable("t1"),
            namedTable("t2"),
            None,
            InnerJoin,
            Seq(),
            JoinDataType(is_left_struct = false, is_right_struct = false)),
          namedTable("t3"),
          None,
          InnerJoin,
          Seq(),
          JoinDataType(is_left_struct = false, is_right_struct = false)))
      example(
        "FROM (SELECT * FROM t1) t2",
        _.fromClause(),
        SubqueryAlias(Project(namedTable("t1"), Seq(Star(None))), Id("t2"), Seq()))
    }

    "translate WHERE clauses" in {
      example(
        "FROM some_table WHERE 1=1",
        _.selectOptionalClauses(),
        Filter(namedTable("some_table"), Equals(Literal(short = Some(1)), Literal(short = Some(1)))))
    }

    "translate GROUP BY clauses" in {
      example(
        "FROM some_table GROUP BY some_column",
        _.selectOptionalClauses(),
        Aggregate(
          namedTable("some_table"),
          group_type = GroupBy,
          grouping_expressions = Seq(simplyNamedColumn("some_column")),
          pivot = None))

      example(
        query = "FROM t1 PIVOT (AVG(a) FOR d IN('x', 'y'))",
        rule = _.selectOptionalClauses(),
        Aggregate(
          namedTable("t1"),
          group_type = Pivot,
          grouping_expressions = Seq(CallFunction("AVG", Seq(simplyNamedColumn("a")))),
          pivot = Some(Pivot(simplyNamedColumn("d"), Seq(Literal(string = Some("x")), Literal(string = Some("y")))))))

      example(
        query = "FROM t1 PIVOT (COUNT(a) FOR d IN('x', 'y'))",
        rule = _.selectOptionalClauses(),
        Aggregate(
          namedTable("t1"),
          group_type = Pivot,
          grouping_expressions = Seq(CallFunction("COUNT", Seq(simplyNamedColumn("a")))),
          pivot = Some(Pivot(simplyNamedColumn("d"), Seq(Literal(string = Some("x")), Literal(string = Some("y")))))))

      example(
        query = "FROM t1 PIVOT (MIN(a) FOR d IN('x', 'y'))",
        rule = _.selectOptionalClauses(),
        Aggregate(
          namedTable("t1"),
          group_type = Pivot,
          grouping_expressions = Seq(CallFunction("MIN", Seq(simplyNamedColumn("a")))),
          pivot = Some(Pivot(simplyNamedColumn("d"), Seq(Literal(string = Some("x")), Literal(string = Some("y")))))))
    }

    "translate ORDER BY clauses" in {
      example(
        "FROM some_table ORDER BY some_column",
        _.selectOptionalClauses(),
        Sort(namedTable("some_table"), Seq(SortOrder(Id("some_column"), Ascending, NullsLast)), is_global = false))
      example(
        "FROM some_table ORDER BY some_column ASC",
        _.selectOptionalClauses(),
        Sort(namedTable("some_table"), Seq(SortOrder(Id("some_column"), Ascending, NullsLast)), is_global = false))
      example(
        "FROM some_table ORDER BY some_column ASC NULLS FIRST",
        _.selectOptionalClauses(),
        Sort(namedTable("some_table"), Seq(SortOrder(Id("some_column"), Ascending, NullsFirst)), is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC",
        _.selectOptionalClauses(),
        Sort(namedTable("some_table"), Seq(SortOrder(Id("some_column"), Descending, NullsFirst)), is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC NULLS LAST",
        _.selectOptionalClauses(),
        Sort(namedTable("some_table"), Seq(SortOrder(Id("some_column"), Descending, NullsLast)), is_global = false))
      example(
        "FROM some_table ORDER BY some_column DESC NULLS FIRST",
        _.selectOptionalClauses(),
        Sort(namedTable("some_table"), Seq(SortOrder(Id("some_column"), Descending, NullsFirst)), is_global = false))

    }

    "translate SAMPLE clauses" in {
      examples(
        Seq("t1 SAMPLE (1)", "t1 TABLESAMPLE (1)", "t1 SAMPLE BERNOULLI (1)", "t1 TABLESAMPLE BERNOULLI (1)"),
        _.tableSource(),
        TableSample(namedTable("t1"), RowSamplingProbabilistic(BigDecimal(1)), None))

      examples(
        Seq(
          "t1 SAMPLE (1 ROWS)",
          "t1 TABLESAMPLE (1 ROWS)",
          "t1 SAMPLE BERNOULLI (1 ROWS)",
          "t1 TABLESAMPLE BERNOULLI (1 ROWS)"),
        _.tableSource(),
        TableSample(namedTable("t1"), RowSamplingFixedAmount(BigDecimal(1)), None))

      examples(
        Seq("t1 SAMPLE BLOCK (1)", "t1 TABLESAMPLE BLOCK (1)", "t1 SAMPLE SYSTEM (1)", "t1 TABLESAMPLE SYSTEM (1)"),
        _.tableSource(),
        TableSample(namedTable("t1"), BlockSampling(BigDecimal(1)), None))

      examples(
        Seq("t1 SAMPLE (1) SEED (1234)", "t1 SAMPLE (1) REPEATABLE (1234)"),
        _.tableSource(),
        TableSample(namedTable("t1"), RowSamplingProbabilistic(BigDecimal(1)), Some(BigDecimal(1234))))
    }

    "translate combinations of the above" in {
      example(
        "FROM some_table WHERE 1=1 GROUP BY some_column",
        _.selectOptionalClauses(),
        Aggregate(
          child = Filter(namedTable("some_table"), Equals(Literal(short = Some(1)), Literal(short = Some(1)))),
          group_type = GroupBy,
          grouping_expressions = Seq(simplyNamedColumn("some_column")),
          pivot = None))

      example(
        "FROM some_table WHERE 1=1 GROUP BY some_column ORDER BY some_column NULLS FIRST",
        _.selectOptionalClauses(),
        Sort(
          Aggregate(
            child = Filter(namedTable("some_table"), Equals(Literal(short = Some(1)), Literal(short = Some(1)))),
            group_type = GroupBy,
            grouping_expressions = Seq(simplyNamedColumn("some_column")),
            pivot = None),
          Seq(SortOrder(Id("some_column"), Ascending, NullsFirst)),
          is_global = false))

      example(
        "FROM some_table WHERE 1=1 ORDER BY some_column NULLS FIRST",
        _.selectOptionalClauses(),
        Sort(
          Filter(namedTable("some_table"), Equals(Literal(short = Some(1)), Literal(short = Some(1)))),
          Seq(SortOrder(Id("some_column"), Ascending, NullsFirst)),
          is_global = false))
    }

    "translate CTE definitions" in {

      example(
        "WITH a AS (SELECT x, y FROM d)",
        _.withExpression(),
        CTEDefinition("a", Seq(), Project(namedTable("d"), Seq(simplyNamedColumn("x"), simplyNamedColumn("y")))))

      example(
        "WITH a (b, c) AS (SELECT x, y FROM d)",
        _.withExpression(),
        CTEDefinition(
          "a",
          Seq(simplyNamedColumn("b"), simplyNamedColumn("c")),
          Project(namedTable("d"), Seq(simplyNamedColumn("x"), simplyNamedColumn("y")))))
    }

    "translate QUALIFY clauses" in {
      example(
        "FROM qt QUALIFY ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) = 1",
        _.selectOptionalClauses(),
        Filter(
          input = namedTable("qt"),
          condition = Equals(
            Window(
              window_function = CallFunction("ROW_NUMBER", Seq()),
              partition_spec = Seq(Id("p")),
              sort_order = Seq(SortOrder(Id("o"), Ascending, NullsLast)),
              frame_spec = None),
            Literal(short = Some(1)))))
    }

    "translate SELECT DISTINCT clauses" in {
      example(
        "SELECT DISTINCT a, b AS bb FROM t",
        _.selectStatement(),
        Project(
          Deduplicate(
            namedTable("t"),
            column_names = Seq(Id("a"), Id("bb")),
            all_columns_as_keys = false,
            within_watermark = false),
          Seq(simplyNamedColumn("a"), Alias(simplyNamedColumn("b"), Seq(Id("bb")), None))))

    }

    "translate SELECT TOP clauses" in {
      example(
        "SELECT TOP 42 a FROM t",
        _.selectStatement(),
        Project(Limit(namedTable("t"), Literal(short = Some(42))), Seq(simplyNamedColumn("a"))))

      example(
        "SELECT DISTINCT TOP 42 a FROM t",
        _.selectStatement(),
        Project(
          Limit(
            Deduplicate(namedTable("t"), Seq(Id("a")), all_columns_as_keys = false, within_watermark = false),
            Literal(short = Some(42))),
          Seq(simplyNamedColumn("a"))))
    }

    "translate VALUES clauses as object references" in {
      example(
        "VALUES ('a', 1), ('b', 2)",
        _.objectRef(),
        Values(
          Seq(
            Seq(Literal(string = Some("a")), Literal(short = Some(1))),
            Seq(Literal(string = Some("b")), Literal(short = Some(2))))))
    }

    "translate table functions as object references" in {
      example(
        "TABLE(some_func(some_arg))",
        _.objectRef(),
        TableFunction(
          UnresolvedFunction("some_func", Seq(Id("some_arg")), is_distinct = false, is_user_defined_function = false)))

      example(
        "TABLE(some_func(some_arg)) t(c1, c2, c3)",
        _.objectRef(),
        SubqueryAlias(
          TableFunction(
            UnresolvedFunction(
              "some_func",
              Seq(Id("some_arg")),
              is_distinct = false,
              is_user_defined_function = false)),
          Id("t"),
          Seq(Id("c1"), Id("c2"), Id("c3"))))

    }

    "translate LATERAL FLATTEN object references" in {
      example(
        "LATERAL FLATTEN (input => some_col, OUTER => true)",
        _.objectRef(),
        Lateral(
          TableFunction(
            CallFunction(
              "FLATTEN",
              Seq(
                snowflake.NamedArgumentExpression("INPUT", Id("some_col")),
                snowflake.NamedArgumentExpression("OUTER", Literal(boolean = Some(true))))))))

      example(
        "LATERAL FLATTEN (input => some_col) AS t",
        _.objectRef(),
        SubqueryAlias(
          Lateral(
            TableFunction(CallFunction("FLATTEN", Seq(snowflake.NamedArgumentExpression("INPUT", Id("some_col")))))),
          Id("t"),
          Seq()))
    }
  }

  "Unparsed input" should {
    "be reported as UnresolvedRelation" in {
      example("MATCH_RECOGNIZE()", _.matchRecognize(), UnresolvedRelation("MATCH_RECOGNIZE()"))
    }
  }

  "SnowflakeRelationBuilder.translateJoinType" should {
    "handle unresolved join type" in {
      val outerJoin = mock[OuterJoinContext]
      val joinType = mock[JoinTypeContext]
      when(joinType.outerJoin()).thenReturn(outerJoin)
      astBuilder.translateJoinType(joinType) shouldBe UnspecifiedJoin
      verify(outerJoin).LEFT()
      verify(outerJoin).RIGHT()
      verify(outerJoin).FULL()
      verify(joinType, times(4)).outerJoin()
    }
  }
}
