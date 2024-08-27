package com.databricks.labs.remorph

import com.databricks.labs.remorph.graph.Node
import org.scalatest.funsuite.AnyFunSuite
import com.databricks.labs.remorph.transpilers.{BaseTranspiler, Parser, SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler}
import org.scalatest.prop.TableDrivenPropertyChecks

class SnowflakeToDatabricksTranspilerTest extends RootTableIdentifierTest {
  override def parser: Parser = new SnowflakeToDatabricksTranspiler()
}

class TSqlToDatabricksTranspilerTest extends RootTableIdentifierTest {
  override def parser: Parser = new TSqlToDatabricksTranspiler()
}

trait RootTableIdentifierTest extends AnyFunSuite with TableDrivenPropertyChecks {

  def parser: Parser

  test("processQuery should correctly process SQL and update Lineage Insert Select") {
    val sql =
      """INSERT INTO output_table AS SELECT col1, col2
        |FROM input_table_1 JOIN input_table_2
        |ON input_table_1.col1 = input_table_2.col1""".stripMargin
    val rootTableIdentifier = new RootTableIdentifier(parser, Seq(sql))

    val resultDAG = rootTableIdentifier.generateLineage()
    val roots = Set(Node(None, "default", "input_table_1"), Node(None, "default", "input_table_2"))
    val expectedNodes = Set(Node(None, "default", "output_table")) ++ roots

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.roots == roots)
  }

  test("process query should correctly process sql and update Lineage Insert Scalar Subquery") {
    if (parser.isInstanceOf[TSqlToDatabricksTranspiler]) {
      // Update from is not implemented in TSQL
      info("Skipping test for TSqlToDatabricksTranspiler")
      cancel()
    }

    val sql =
      """INSERT INTO output_table_main SELECT * FROM table2
        |INNER JOIN table3 ON table2.id = table3.id
        |WHERE table2.id IN (SELECT id FROM table4);""".stripMargin

    val rootTableIdentifier = new RootTableIdentifier(parser, Seq(sql))

    val resultDAG = rootTableIdentifier.generateLineage()
    val roots = Set(Node(None, "default", "table2"), Node(None, "default", "table3"), Node(None, "default", "table4"))
    val expectedNodes = roots ++ Set(Node(None, "default", "output_table_main"))

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.roots == roots)
  }

  test("process query should correctly process sql and update Lineage Update query") {
    val sql =
      """UPDATE table1
        |SET col1 = 1
        |WHERE col2 = 2""".stripMargin

    val rootTableIdentifier = new RootTableIdentifier(parser, Seq(sql))

    val resultDAG = rootTableIdentifier.generateLineage()
    val expectedNodes = Set(Node(None, "default", "table1"))
    val roots = Set(Node(None, "default", "table1"))

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.roots == roots)

  }

  test("process query should correctly process sql and update Lineage Update From query") {
    if (parser.isInstanceOf[TSqlToDatabricksTranspiler]) {
      // Update from is not implemented in TSQL
      info("Skipping test for TSqlToDatabricksTranspiler")
      cancel()
    }

    val sql =
      """UPDATE c.s.t1
        |SET column1 = t1.column1 + t2.column1, column3 = 'success'
        |FROM c.s.t2
        |WHERE t1.key = t2.t1_key and t1.column1 < 10;""".stripMargin

    val rootTableIdentifier = new RootTableIdentifier(parser, Seq(sql))

    val resultDAG = rootTableIdentifier.generateLineage()
    val expectedNodes = Set(Node(Some("c"), "s", "t1"), Node(Some("c"), "s", "t2"))
    val roots = Set(Node(Some("c"), "s", "t2"))

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.roots == roots)

  }

  test("process query should correctly process sql and update From query Lineage") {
    if (parser.isInstanceOf[TSqlToDatabricksTranspiler]) {
      // Update from is not implemented in TSQL
      info("Skipping test for TSqlToDatabricksTranspiler")
      cancel()
    }

    val sql =
      """UPDATE t1
        |SET column1 = t1.column1 + t2.column1, column3 = 'success'
        |FROM t2
        |WHERE t1.key = t2.t1_key and t1.column1 < 10;""".stripMargin

    val rootTableIdentifier = new RootTableIdentifier(parser, Seq(sql))

    val resultDAG = rootTableIdentifier.generateLineage()
    val expectedNodes = Set(Node(None, "default", "t1"), Node(None, "default", "t2"))
    val parent = Set(Node(None, "default", "t2"))

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.getImmediateParents("t1") == parent)

  }

  test("process query should correctly process sql and create- From query Lineage") {

    if (parser.isInstanceOf[BaseTranspiler]) {
      // Create Table from is not implemented in TSQL
      info("Skipping test for TSqlToDatabricksTranspiler")
      cancel()
    }

    val sql =
      """CREATE TABLE output_table AS SELECT col1, col2
        |FROM input_table_1 JOIN input_table_2
        |ON input_table_1.col1 = input_table_2.col1""".stripMargin

    val rootTableIdentifier = new RootTableIdentifier(parser, Seq(sql))

    val resultDAG = rootTableIdentifier.generateLineage()
    val expectedNodes = Set(
      Node(None, "default", "output_table"),
      Node(None, "default", "input_table_1"),
      Node(None, "default", "input_table_2"))
    val roots = Set(Node(None, "default", "input_table_1"), Node(None, "default", "input_table_2"))

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.roots == roots)

  }

  test("process a query set and generate Lineage") {
    val sql = Seq(
      """SELECT col1, col2
      |FROM input_table_1 JOIN
      |(SELECT col1 FROM input_table_3) as input_table_2
      |ON input_table_1.col1 = input_table_2.col1""".stripMargin,
      """INSERT INTO table1 SELECT * FROM table2 INNER JOIN
      |table3 ON table2.id = table3.id WHERE table2.id in (SELECT id FROM table4)""".stripMargin,
      "INSERT INTO table2 SELECT * FROM table4",
      "INSERT INTO table5 SELECT * FROM table3 JOIN table4 ON table3.id = table4.id")

    val rootTableIdentifier = new RootTableIdentifier(parser, sql)

    val resultDAG = rootTableIdentifier.generateLineage()
    val expectedNodes = Set(
      Node(None, "default", "input_table_1"),
      Node(None, "default", "input_table_3"),
      Node(None, "default", "table1"),
      Node(None, "default", "table2"),
      Node(None, "default", "table3"),
      Node(None, "default", "table4"),
      Node(None, "default", "table5"))
    val roots = Set(
      Node(None, "default", "input_table_1"),
      Node(None, "default", "input_table_3"), // table 2 is not a base root
      Node(None, "default", "table3"),
      Node(None, "default", "table4"))

    assert(resultDAG.sorted == expectedNodes)
    assert(resultDAG.roots == roots)
  }
}
