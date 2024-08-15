package com.databricks.labs.remorph

import org.scalatest.funsuite.AnyFunSuite

class RootTableIdentifierTest extends AnyFunSuite {

  test("processQuery should correctly process SQL and update DAG Insert Select") {
    val engine = "snowflake"
    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin
    val dag = new DAG()
    val rootTableIdentifier = new RootTableIdentifier(engine)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_2"))
    val expectedEdges =
      Set(Edge(Node("input_table_1"), Node("output_table")), Edge(Node("input_table_2"), Node("output_table")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("processQuery should correctly process SQL and update DAG Insert Join ") {
    val engine = "tsql"
    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN
                |(SELECT col1 FROM input_table_3) as input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin
    val dag = new DAG()
    val rootTableIdentifier = new RootTableIdentifier(engine)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_3"))
    val expectedEdges =
      Set(Edge(Node("input_table_1"), Node("output_table")), Edge(Node("input_table_3"), Node("output_table")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  // TODO Add tests for Create Table AS Select Queries

}
