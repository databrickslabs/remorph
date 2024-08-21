package com.databricks.labs.remorph

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.Transpiler
// scalastyle:off
case class ChildActionMap(name: String, action: Action.Operation)
class RootTableIdentifier(transpiler: Transpiler) {

  def processQuery(sql: String, graph: Lineage): Lineage = {
    val parsedSql = transpiler.parse(sql)
    findTables(graph, parsedSql)
  }

  private def getTableFromExpression(p: ir.Expression): Set[String] = {
    p.collect { case exp: ir.ScalarSubquery =>
      fetchTableName(exp.relation)
    }.toSet
  }

  private def getTableList(p: ir.LogicalPlan): Set[String] = {
    p.collect { case nt: ir.NamedTable =>
      nt.unparsed_identifier
    }.toSet
  }

  private def fetchTableName(p: ir.LogicalPlan): String = {
    p.collectFirst { case nt: ir.NamedTable =>
      nt.unparsed_identifier
    }.get
  }

  private def findTables(graph: Lineage, plan: ir.LogicalPlan): Lineage = {
    var child: ChildActionMap = null
    var parent = Set.empty[String]

    def updateChild(target: ir.LogicalPlan, action: Action.Operation): Unit = {
      child = ChildActionMap(fetchTableName(target), action)
    }

    def collectTables(node: ir.LogicalPlan): Unit = {

      node match {
        case c: ir.CreateTable => // TODO be implemented for CTAS
        case i: ir.InsertIntoTable => updateChild(i.target, Action.Write)
        case d: ir.DeleteFromTable => updateChild(d.target, Action.Delete)
        case u: ir.UpdateTable => updateChild(u.target, Action.Update)
        case m: ir.MergeIntoTable => updateChild(m.targetTable, Action.Update)
        case p: ir.Project => parent = parent ++ getTableList(p)
        case i: ir.Join => parent = parent ++ getTableList(i)
        case sub: ir.SubqueryAlias => parent = parent ++ getTableList(sub)
        case f: ir.Filter => parent = parent ++ getTableFromExpression(f.condition)
        case _ => () // do Nothing
      }

      node.children.foreach(collectTables)
    }
    collectTables(plan)

    graph.addNode(Node(child.name))
    parent.toList.sorted.foreach(p => {
      graph.addNode(Node(p))
      graph.addEdge(Node(p), Node(child.name), child.action)
    })
    graph
  }

}
