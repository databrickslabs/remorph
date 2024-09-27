package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{QueryHistory, TableDefinition}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.{Result, SourceCode}
import com.typesafe.scalalogging.LazyLogging
import com.databricks.labs.remorph.parsers.{intermediate => ir}

protected case class Node(tableDefinition: TableDefinition, metadata: Map[String, Set[String]])
protected case class Edge(from: TableDefinition, to: TableDefinition, metadata: Map[String, String])

class TableDependencyGraph(parser: PlanParser[_]) extends DependencyGraph with LazyLogging {
  private val nodes = scala.collection.mutable.Set.empty[Node]
  private val edges = scala.collection.mutable.Set.empty[Edge]

  override protected def addNode(id: TableDefinition, metadata: Map[String, String]): Unit = {
    // Metadata list of query ids and add node only if it is not already present.
    // for Example if a table is used in multiple queries, we need to consolidate the metadata
    // here we are storing only query hash id as metadata not the query itself
    val existingNode = nodes.find(_.tableDefinition == id)
    existingNode match {
      case Some(node) =>
        val consolidatedMetadata = (node.metadata.toSeq ++ metadata.toSeq)
          .groupBy(_._1)
          .mapValues(_.map(_._2.toString).toSet)
        nodes -= node
        nodes += node.copy(metadata = consolidatedMetadata)
      case None =>
        nodes += Node(id, metadata.mapValues(Set(_)))
    }
  }

  override protected def addEdge(from: TableDefinition, to: TableDefinition, metadata: Map[String, String]): Unit = {
    edges += Edge(from, to, metadata)
  }

  // protected override def getNodes: Set[TableDefinition] = nodes.map(_.tableDefinition).toSet

  // protected override def getEdges: Set[(TableDefinition, TableDefinition)] =
  // edges.map(edge => (edge.from, edge.to)).toSet

  private def walkWithParent(plan: ir.LogicalPlan)(f: (ir.LogicalPlan, Option[ir.LogicalPlan]) => Unit): Unit = {
    def recurse(node: ir.LogicalPlan, parent: Option[ir.LogicalPlan]): Unit = {
      f(node, parent)
      node.children.foreach(child => recurse(child, Some(node)))
    }
    recurse(plan, None)
  }

  private def getTableName(plan: ir.LogicalPlan): Option[String] = {
    plan collectFirst { case x: ir.NamedTable =>
      x.unparsed_identifier
    }
  }

  private def generateEdges(plan: ir.LogicalPlan, tableDefinition: Seq[TableDefinition], queryId: String): Unit = {
    walkWithParent(plan) {
      case (node: ir.NamedTable, Some(parent)) =>
        parent match {
          case _: ir.Project | _: ir.Join | _: ir.SubqueryAlias | _: ir.Filter =>
            val fromTable = tableDefinition.filter(_.table == node.unparsed_identifier).head
            val toTable = tableDefinition.filter(_.table == getTableName(parent).getOrElse("None")).head
            // TODO figure out a simpler way to add Action
            addEdge(fromTable, toTable, Map("query" -> queryId, "action" -> "action"))
          case _ => // Do nothing for other parent types
        }
      case _ => // Do nothing for other node types
    }
  }

  def buildDependancy(queryHistory: QueryHistory, tableDefinition: Seq[TableDefinition]): Unit = {
    queryHistory.queries.foreach { query =>
      val plan = parser.parse(SourceCode(query.source)).flatMap(parser.visit)
      plan match {
        case Result.Success(plan) =>
          plan collect { case x: ir.NamedTable =>
            addNode(tableDefinition.filter(_.table == x.unparsed_identifier).head, Map("query" -> query.id))
          }
          generateEdges(plan, tableDefinition, query.id)

        case _ => logger.warn(s"Failed to produce plan from query: ${query.source}")
      }
    }
  }

  // TODO Implement logic for fetching edges(parents) only upto certain level
  override def getRoot(table: String, level: Int = 0): TableDefinition = {
    def findRoot(node: Node, currentLevel: Int): Node = {
      if (currentLevel == level || edges.forall(_.to != node.tableDefinition)) {
        node
      } else {
        val upstreamNodes = edges
          .filter(_.to == node.tableDefinition)
          .map(edge => nodes.find(_.tableDefinition == edge.from).get)
        findRoot(upstreamNodes.head, currentLevel + 1) // Assuming a single upstream path for simplicity
      }
    }
    val targetNode = nodes
      .find(_.tableDefinition.table == table)
      .getOrElse(throw new NoSuchElementException(s"No table $table found"))
    findRoot(targetNode, 0).tableDefinition
  }

  override def getUpstreamTables(table: String): Set[TableDefinition] = {
    val targetNode = nodes.find(_.tableDefinition.table == table)
    targetNode match {
      case Some(node) => edges.filter(_.to == node.tableDefinition).map(_.from).toSet
      case None => Set.empty[TableDefinition]
    }
  }

  override def getDownstreamTables(table: String): Set[TableDefinition] = {
    val targetNode = nodes.find(_.tableDefinition.table == table)
    targetNode match {
      case Some(node) => edges.filter(_.from == node.tableDefinition).map(_.to).toSet
      case None => Set.empty[TableDefinition]
    }
  }

}
