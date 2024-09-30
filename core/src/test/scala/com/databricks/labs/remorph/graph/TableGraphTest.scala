package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.TableDefinition
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

import java.sql.Timestamp
import java.time.Duration
import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory}
import com.databricks.labs.remorph.parsers.intermediate.{IntegerType, StringType, StructField}

class TableGraphTest extends AnyFlatSpec with Matchers {
  private val parser = new SnowflakePlanParser()
  private val queryHistory = QueryHistory(
    Seq(
      ExecutedQuery(
        "query1",
        new Timestamp(System.currentTimeMillis()),
        "CREATE TABLE table1 (col1 INT, col2 STRING)",
        Duration.ofSeconds(30),
        "user1"),
      ExecutedQuery(
        "query2",
        new Timestamp(System.currentTimeMillis()),
        "INSERT INTO table2 (col1, col2) VALUES (1, 'value1')",
        Duration.ofSeconds(45),
        "user2"),
      ExecutedQuery(
        "query3",
        new Timestamp(System.currentTimeMillis()),
        "SELECT * FROM table3 JOIN table4 ON table3.id = table4.id",
        Duration.ofSeconds(60),
        "user3"),
      ExecutedQuery(
        "query4",
        new Timestamp(System.currentTimeMillis()),
        "SELECT col1, (SELECT MAX(col2) FROM table5) AS max_col2 FROM table5",
        Duration.ofSeconds(25),
        "user4"),
      ExecutedQuery(
        "query5",
        new Timestamp(System.currentTimeMillis()),
        "WITH cte AS (SELECT col1 FROM table5) SELECT * FROM cte",
        Duration.ofSeconds(35),
        "user5"),
      ExecutedQuery(
        "query6",
        new Timestamp(System.currentTimeMillis()),
        "INSERT INTO table1 (col1, col2) VALUES (2, 'value2')",
        Duration.ofSeconds(40),
        "user1"),
      ExecutedQuery(
        "query7",
        new Timestamp(System.currentTimeMillis()),
        "MERGE INTO table2 USING table3 source_table ON table2.id = source_table.id " +
          "WHEN MATCHED THEN UPDATE SET table2.col1 = source_table.col1",
        Duration.ofSeconds(50),
        "user2"),
      ExecutedQuery(
        "query8",
        new Timestamp(System.currentTimeMillis()),
        "UPDATE table3 SET col1 = 'new_value' WHERE col2 = 'condition'",
        Duration.ofSeconds(55),
        "user3"),
      ExecutedQuery(
        "query9",
        new Timestamp(System.currentTimeMillis()),
        "DELETE FROM table4 WHERE col1 = 'value_to_delete'",
        Duration.ofSeconds(20),
        "user4"),
      ExecutedQuery(
        "query10",
        new Timestamp(System.currentTimeMillis()),
        "SELECT * FROM table5 WHERE col1 = 'some_value'",
        Duration.ofSeconds(65),
        "user5")))

  private val tableDefinitions = Seq(
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

  "TableDependencyGraph" should "add nodes correctly" in {

    val graph = new TableGraph(parser, tableDefinitions)
    graph.buildDependency(queryHistory)
    val nodes = graph.getRoot("table1")
    print(nodes)
  }

}
