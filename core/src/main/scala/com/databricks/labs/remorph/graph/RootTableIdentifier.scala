package com.databricks.labs.remorph

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.graph.{Action, Lineage, Node}
import com.databricks.labs.remorph.transpilers.Parser

private case class FullTableIdentifier(catalog: Option[String], schema: String, table: String)
private case class ChildParentMap(
    child: FullTableIdentifier,
    action: Action.Operation,
    parent: Set[FullTableIdentifier])

class RootTableIdentifier(parser: Parser, queries: Seq[String]) {

  def generateLineage(): Lineage = {
    val graph = new Lineage()
    val lineageMap = queries.map(q => processQuery(q)).flatten
    lineageMap.foreach(l => {
      val child = l.child
      val parent = l.parent
      val action = l.action
      if (child != null) {
        graph.addNode(Node(child.catalog, child.schema, child.table))
      }

      parent.toList
        .sortBy(_.table)
        .foreach(p => {
          graph.addNode(Node(p.catalog, p.schema, p.table))
          // merge IR nodes will produce the same parent and child
          val from = Node(p.catalog, p.schema, p.table)
          var to = Node(None, "default", "None")
          if (child != null) {
            to = Node(child.catalog, child.schema, child.table)
          }
          graph.addEdge(from, to, action)
        })
    })

    graph

  }

  private def processQuery(sql: String): Seq[ChildParentMap] = {
    val parsedSql = parser.parse(sql)
    parsedSql.children.map(p => findTables(p))
  }

  private def getFqn(name: String): FullTableIdentifier = {
    val parts = name.split("\\.")
    if (parts.length == 1) {
      FullTableIdentifier(None, "default", parts(0))
    } else if (parts.length == 2) {
      FullTableIdentifier(None, parts(0), parts(1))
    } else {
      FullTableIdentifier(Some(parts(0)), parts(1), parts(2))
    }
  }

  private def getTableFromExpression(p: ir.Expression): Set[FullTableIdentifier] = {
    // TODO Tackle Unresolved Expressions
    p.collect { case e: ir.ScalarSubquery =>
      fetchTableName(e.relation)
    }.toSet
  }

  private def getTableList(p: ir.LogicalPlan): Set[FullTableIdentifier] = {
    p.collect { case nt: ir.NamedTable =>
      getFqn(nt.unparsed_identifier)
    }.toSet
  }

  private def fetchTableName(p: ir.LogicalPlan): FullTableIdentifier = {
    p.collectFirst { case nt: ir.NamedTable =>
      getFqn(nt.unparsed_identifier)
    }.get
  }

  private def findTables(plan: ir.LogicalPlan): ChildParentMap = {
    var child: FullTableIdentifier = null
    var action: Action.Operation = Action.Read
    var parent = Set.empty[FullTableIdentifier]

    def collectTables(node: ir.LogicalPlan): Unit = {

      node match {
        case c: ir.CreateTable =>
          child = getFqn(c.table_name)
          action = Action.Write // TODO implement for CTAS
        case i: ir.InsertIntoTable =>
          child = fetchTableName(i.target)
          action = Action.Write
        case d: ir.DeleteFromTable =>
          child = fetchTableName(d.target)
          action = Action.Delete
        case u: ir.UpdateTable =>
          child = fetchTableName(u.target)
          action = Action.Update
        case m: ir.MergeIntoTable =>
          child = fetchTableName(m.targetTable)
          action = Action.Merge
        case p: ir.Project => parent = parent ++ getTableList(p)
        case i: ir.Join => parent = parent ++ getTableList(i)
        case sub: ir.SubqueryAlias => parent = parent ++ getTableList(sub)
        case f: ir.Filter => parent = parent ++ getTableFromExpression(f.condition)
        case null => () // Parser Error eventually when parser is fixed there shouldn't be any null pointer exception
        case _ => () // do Nothing
      }

      node.children.foreach(collectTables)
    }
    collectTables(plan)

    ChildParentMap(child, action, parent)
  }

}
