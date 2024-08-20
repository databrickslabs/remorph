/*
package com.databricks.labs.remorph

import org.scalatest.funsuite.AnyFunSuite
import com.databricks.labs.remorph.transpilers.{SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler}

class RootTableIdentifierTest extends AnyFunSuite {

  test("processQuery should correctly process SQL and update DAG Insert Select") {
    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin
    val dag = new Lineage()
    val transpiler = new SnowflakeToDatabricksTranspiler()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_2"))
    val expectedEdges =
      Set(Edge(Node("input_table_1"), Node("output_table"), Action.Read),
        Edge(Node("input_table_2"), Node("output_table"), Action.Read))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("processQuery should correctly process SQL and update DAG Insert Join ") {
    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN
                |(SELECT col1 FROM input_table_3) as input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin

    val dag = new Lineage()
    val transpiler = new TSqlToDatabricksTranspiler()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_3"))
    val expectedEdges =
      Set(Edge(Node("input_table_1"), Node("output_table"), Action.Read),
        Edge(Node("input_table_3"), Node("output_table"), Action.Read))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  // TODO Add tests for Create Table AS Select Queries

}
*/
