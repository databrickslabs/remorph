package com.databricks.labs.remorph

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.Transpiler

class RootTableIdentifier(transpiler: Transpiler) {

  def processQuery(sql: String, dag: Lineage): Lineage = {
    val parsedSql = transpiler.parse(sql)
    findTables(dag, parsedSql)
  }

  private def getTablName(p: ir.LogicalPlan): Set[String] = {
    p.find(_.isInstanceOf[ir.NamedTable]).map(_.asInstanceOf[ir.NamedTable].unparsed_identifier).toSet
  }

  private def findTables(dag: Lineage, plan: ir.LogicalPlan): Lineage = {
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
