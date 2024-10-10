package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory, QuerySpec, TableDefinition}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

import java.sql.Timestamp
import java.time.Duration
import com.databricks.labs.remorph.intermediate.{IntegerType, StringType, StructField}

class TableGraphTest extends AnyFlatSpec with Matchers {
  private val parser = new SnowflakePlanParser()
  private val queryHistory = QueryHistory(
    Seq(
      ExecutedQuery(
        "query1",
        "INSERT INTO table1 SELECT col1, col2 FROM table2 INNER JOIN table3 on table2.id = table3.id",
        QuerySpec()),
      ExecutedQuery(
        "query2",
        "INSERT INTO table2 (col1, col2) VALUES (1, 'value1')",
        QuerySpec()),
      ExecutedQuery(
        "query3",
        "SELECT * FROM table3 JOIN table4 ON table3.id = table4.id",
        QuerySpec()),
      ExecutedQuery(
        "query4",
        "SELECT col1, (SELECT MAX(col2) FROM table5) AS max_col2 FROM table5",
        QuerySpec()),
      ExecutedQuery(
        "query5",
        "WITH cte AS (SELECT col1 FROM table5) SELECT * FROM cte",
        QuerySpec()),
      ExecutedQuery(
        "query6",
        "INSERT INTO table1 (col1, col2) VALUES (2, 'value2')",
        QuerySpec()),
      ExecutedQuery(
        "query7",
        """MERGE INTO table2 USING table3 source_table ON table2.id = source_table.id
          |WHEN MATCHED THEN UPDATE SET table2.col1 = source_table.col1""".stripMargin,
        QuerySpec()),
      ExecutedQuery(
        "query8",
        "UPDATE table3 SET col1 = 'new_value' WHERE col2 = 'condition'",
        QuerySpec()),
      ExecutedQuery(
        "query9",
        "DELETE FROM table4 WHERE col1 = 'value_to_delete'",
        QuerySpec()),
      ExecutedQuery(
        "query10",
        "INSERT INTO table2 SELECT * FROM table5 WHERE col1 = 'some_value'",
        QuerySpec())))

  private val tableDefinitions = Set(
    TableDefinition(
      catalog = "catalog1",
      schema = "schema1",
      table = "table1",
      columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
      sizeGb = 10),
    TableDefinition(
      catalog = "catalog2",
      schema = "schema2",
      table = "table2",
      columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
      sizeGb = 20),
    TableDefinition(
      catalog = "catalog3",
      schema = "schema3",
      table = "table3",
      columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
      sizeGb = 30),
    TableDefinition(
      catalog = "catalog4",
      schema = "schema4",
      table = "table4",
      columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
      sizeGb = 40),
    TableDefinition(
      catalog = "catalog5",
      schema = "schema5",
      table = "table5",
      columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
      sizeGb = 50))
  val graph = new TableGraph(parser)
  graph.buildDependency(queryHistory, tableDefinitions)

  "TableDependencyGraph" should "add nodes correctly" in {
    val roots = graph.getRootTables()
    assert(roots.size == 3)
    assert(roots.map(x => x.table).toList.sorted.toSet == Set("table3", "table4", "table5"))

  }

  "TableDependencyGraph" should "return correct upstream tables" in {
    val upstreamTables = graph.getUpstreamTables(
      TableDefinition(
        catalog = "catalog1",
        schema = "schema1",
        table = "table1",
        columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
        sizeGb = 10))
    assert(upstreamTables.map(_.table).toList.sorted == List("table2", "table3", "table5"))
  }

  "TableDependencyGraph" should "return correct downstream tables" in {
    val downstreamTables = graph.getDownstreamTables(
      TableDefinition(
        catalog = "catalog5",
        schema = "schema5",
        table = "table5",
        columns = Seq(StructField("col1", IntegerType, true), StructField("col2", StringType, false)),
        sizeGb = 50))
    assert(downstreamTables.map(_.table).toList.sorted == List("table1", "table2"))
  }

}
