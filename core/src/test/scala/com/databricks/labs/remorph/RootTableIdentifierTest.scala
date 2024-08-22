package com.databricks.labs.remorph

import org.scalatest.funsuite.AnyFunSuite
import com.databricks.labs.remorph.transpilers.{SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler, Transpiler}
import org.scalatest.prop.TableDrivenPropertyChecks

class SnowflakeToDatabricksTranspilerTest extends RootTableIdentifierTest {
  override def transpiler: Transpiler = new SnowflakeToDatabricksTranspiler()
}

class TSqlToDatabricksTranspilerTest extends RootTableIdentifierTest {
  override def transpiler: Transpiler = new TSqlToDatabricksTranspiler()
}

trait RootTableIdentifierTest extends AnyFunSuite with TableDrivenPropertyChecks{

  def transpiler: Transpiler

  test("processQuery should correctly process SQL and update Lineage Insert Select") {
    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin
    val dag = new Lineage()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_2"))
    val expectedEdges =
      Set(
        Edge(Node("input_table_1"), Action.Write, Node("output_table")),
        Edge(Node("input_table_2"), Action.Write, Node("output_table")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("processQuery should correctly process SQL and update Lineage Insert Join ") {
    if (transpiler.isInstanceOf[TSqlToDatabricksTranspiler]) {
      // Unsupported expression: UnresolvedExpression table2.idIN(SELECTidFROMtable4) for TSQL
      info("Skipping test for TSqlToDatabricksTranspiler")
      cancel()
    }

    val sql = """INSERT INTO output_table AS SELECT col1, col2
                |FROM input_table_1 JOIN
                |(SELECT col1 FROM input_table_3) as input_table_2
                |ON input_table_1.col1 = input_table_2.col1""".stripMargin

    val dag = new Lineage()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("output_table"), Node("input_table_1"), Node("input_table_3"))
    val expectedEdges =
      Set(
        Edge(Node("input_table_1"), Action.Write, Node("output_table")),
        Edge(Node("input_table_3"), Action.Write, Node("output_table")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("process query should correctly process sql and update Lineage Insert Scalar Subquery") {

    val sql = """INSERT INTO output_table_main SELECT * FROM table2
        |INNER JOIN table3 ON table2.id = table3.id
        |WHERE table2.id IN (SELECT id FROM table4);""".stripMargin

    val dag = new Lineage()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("table2"), Node("table3"), Node("table4"), Node("output_table_main"))
    val expectedEdges =
      Set(
        Edge(Node("table2"), Action.Write, Node("output_table_main")),
        Edge(Node("table3"), Action.Write, Node("output_table_main")),
        Edge(Node("table4"), Action.Write, Node("output_table_main")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)
  }

  test("process query should correctly process sql and update Lineage Update query") {
    val sql = """UPDATE table1
                |SET col1 = 1
                |WHERE col2 = 2""".stripMargin

    val dag = new Lineage()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("table1"))
    val expectedEdges = Set()

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)

  }

  test("process query should correctly process sql and update Lineage Update From query") {
    if (transpiler.isInstanceOf[TSqlToDatabricksTranspiler]) {
      // Update from is not implemented in TSQL
      info("Skipping test for TSqlToDatabricksTranspiler")
      cancel()
    }

    val sql = """UPDATE t1
                |SET column1 = t1.column1 + t2.column1, column3 = 'success'
                |FROM t2
                |WHERE t1.key = t2.t1_key and t1.column1 < 10;""".stripMargin

    val dag = new Lineage()
    val rootTableIdentifier = new RootTableIdentifier(transpiler)

    val resultDAG = rootTableIdentifier.processQuery(sql, dag)
    val expectedNodes = Set(Node("t1"), Node("t2"))
    val expectedEdges = Set(Edge(Node("t2"), Action.Update, Node("t1")), Edge(Node("t1"), Action.Update, Node("t1")))

    assert(resultDAG.getNodes == expectedNodes)
    assert(resultDAG.getEdges == expectedEdges)

  }

  test("process query should correctly process sql and update Lineage Insert ss Subquery") {

  }


  // TODO Add tests for Create Table AS Select Queries

}
