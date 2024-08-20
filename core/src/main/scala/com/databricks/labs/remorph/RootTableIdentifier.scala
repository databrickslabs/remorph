package com.databricks.labs.remorph

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.Transpiler

class RootTableIdentifier(transpiler: Transpiler) {

  def processQuery(sql: String, graph: Lineage): Lineage = {
    val parsedSql = transpiler.parse(sql)
    findTables(graph, parsedSql)
  }

  private def getTableNode(p: ir.LogicalPlan): Set[Node] = {
    p.collect {
      case nt: ir.NamedTable => Node(nt.unparsed_identifier)
    }.toSet
  }

  private def findTables(graph: Lineage, plan: ir.LogicalPlan): Lineage = {

    plan.collect {
      case nt: ir.NamedTable => nt.unparsed_identifier
      case _ => getTableNode(_)
    }

    graph

  }

}
