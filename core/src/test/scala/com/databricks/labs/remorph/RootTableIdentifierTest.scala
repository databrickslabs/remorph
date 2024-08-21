package com.databricks.labs.remorph

import org.scalatest.funsuite.AnyFunSuite
import com.databricks.labs.remorph.transpilers.{SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler}

class RootTableIdentifierTest extends AnyFunSuite {

  test("processQuery should correctly process SQL and update Lineage Insert Select") {
    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin
    val dag = new Lineage()
    val transpiler = new SnowflakeToDatabricksTranspiler()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_2"))
    val expectedEdges =
      Set(Edge(Node("input_table_1"), Action.Write, Node("output_table")),
        Edge(Node("input_table_2"), Action.Write, Node("output_table")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("processQuery should correctly process SQL and update Lineage Insert Join ") {
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
      Set(Edge(Node("input_table_1"), Action.Write, Node("output_table")),
        Edge(Node("input_table_3"), Action.Write, Node("output_table")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("process query should correctly process sql and update Lineage Insert Scalar Subquery") {
    val sql = """INSERT INTO output_table_main SELECT * FROM table2
        |INNER JOIN table3 ON table2.id = table3.id
        |WHERE table2.id IN (SELECT id FROM table4);""".stripMargin

    val dag = new Lineage()
    val transpiler = new SnowflakeToDatabricksTranspiler()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table_main"), Node("table2"), Node("table3"), Node("table4"))
    val expectedEdges =
      Set(Edge(Node("table2"), Action.Write, Node("output_table_main")),
        Edge(Node("table3"), Action.Write, Node("output_table_main")),
        Edge(Node("table4"), Action.Write, Node("output_table_main")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  // TODO Add tests for Create Table AS Select Queries

}

