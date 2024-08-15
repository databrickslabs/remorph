package com.databricks.labs.remorph

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspilerFactory

import java.io.File
import scala.io.Source

class RootTableIdentifier(engine: String) {

  private val transpiler = TranspilerFactory.getTranspiler(engine)

  def processFile(file: File, dag: DAG): DAG = {
    val source = Source.fromFile(file)
    try {
      val sql = source.getLines().mkString("\n")
      val parsedSql = transpiler.parse(sql)
      findTables(dag, parsedSql)
    } finally {
      source.close()
    }
  }

  private def getTablName(p: ir.LogicalPlan): Set[String] = {
    p.find(_.isInstanceOf[ir.NamedTable]).map(_.asInstanceOf[ir.NamedTable].unparsed_identifier).toSet
  }

  private def findTables(dag: DAG, plan: ir.LogicalPlan): DAG = {
    var child = ""
    var parent = Set.empty[String]

    def collectTables(node: ir.LogicalPlan): Unit = {
      node match {
        case n: ir.InsertIntoTable =>
          child = n.target
            .find(_.isInstanceOf[ir.NamedTable])
            .map(_.asInstanceOf[ir.NamedTable].unparsed_identifier)
            .getOrElse("unknown") // Unknown is when query is a Select Query. May be file name becomes the table name.

        case p: ir.Project => parent = parent ++ getTablName(p)

        case j: ir.Join => parent = parent ++ getTablName(j.left) ++ getTablName(j.right)
        case _ => // Do nothing for other nodes
      }
      node.children.foreach(collectTables)
    }

    collectTables(plan)
    val childNode = Node(child)
    dag.addNode(childNode)
    parent.foreach { parentTable =>
      val parentNode = Node(parentTable)
      dag.addNode(parentNode)
      dag.addEdge(parentNode, childNode)
    }
    dag
  }

}
