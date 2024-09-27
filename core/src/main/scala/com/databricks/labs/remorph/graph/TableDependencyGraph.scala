package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{QueryHistory, TableDefinition}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.{Result, SourceCode}
import com.typesafe.scalalogging.LazyLogging
import com.databricks.labs.remorph.parsers.{intermediate => ir}

class TableDependencyGraph(parser: PlanParser[_]) extends DependencyGraph with LazyLogging {
  private val nodes = scala.collection.mutable.Set.empty[TableDefinition]
  private val edges = scala.collection.mutable.Set.empty[(TableDefinition, TableDefinition)]
  private val nodeMetadata = scala.collection.mutable.Map.empty[TableDefinition, Map[String, Set[String]]]
  private val edgeMetadata = scala.collection.mutable.Map.empty[(TableDefinition, TableDefinition), Map[String, String]]

  override protected def addNode(id: TableDefinition, metadata: Map[String, String]): Unit = {
    // Metadata list of query ids and add node only if it is not already present.
    // for Example if a table is used in multiple queries, we need to consolidate the metadata
    // here we are storing only query hash id as metadata not the query itself
    if (nodes.contains(id)) {
      val existingMetadata = nodeMetadata(id)
      val consolidatedMetadata = (existingMetadata.toSeq ++ metadata.toSeq)
        .groupBy(_._1)
        .mapValues(_.map(_._2.toString).toSet)
      nodeMetadata.update(id, consolidatedMetadata)
    } else {
      nodes += id
      nodeMetadata += id -> metadata.mapValues(Set(_))
    }
  }

  override protected def addEdge(from: TableDefinition, to: TableDefinition, metadata: Map[String, String]): Unit = {
    edges += ((from, to))
    edgeMetadata += ((from, to)) -> metadata
  }

  override protected def getNodes: Set[TableDefinition] = nodes.toSet

  override protected def getEdges: Set[(TableDefinition, TableDefinition)] = edges.toSet

  private def walkWithParent(plan: ir.LogicalPlan)(f: (ir.LogicalPlan, Option[ir.LogicalPlan]) => Unit): Unit = {
    def recurse(node: ir.LogicalPlan, parent: Option[ir.LogicalPlan]): Unit = {
      f(node, parent)
      node.children.foreach(child => recurse(child, Some(node)))
    }
    recurse(plan, None)
  }

  private def generateEdges(plan: ir.LogicalPlan, tableDefinition: Seq[TableDefinition], queryId: String): Unit = {
    walkWithParent(plan) {
      case (node: ir.NamedTable, Some(parent)) =>
        parent match {
          case _: ir.Project | _: ir.Join | _: ir.SubqueryAlias | _: ir.Filter =>
            val fromTable = tableDefinition.filter(_.table == node.unparsed_identifier).head
            val toTable = tableDefinition.filter(_.table == parent.asInstanceOf[ir.NamedTable].unparsed_identifier).head
            // TODO figure out a simpler way to add Action
            addEdge(fromTable, toTable, Map("query" -> queryId, "action" -> "action"))
          case _ => // Do nothing for other parent types
        }
      case _ => // Do nothing for other node types
    }
  }

  def buildGraph(queryHistory: QueryHistory, tableDefinition: Seq[TableDefinition]): Unit = {
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
  override def getRoot(table: String, level: Int): TableDefinition = getNodes
    .find(_.table == table)
    .getOrElse(throw new NoSuchElementException(s"No table ${table} found"))

  override def getUpstreamTables(table: String): Set[TableDefinition] = getEdges.filter(_._2.table == table).map(_._1)

  override def getDownstreamTables(table: String): Set[TableDefinition] = getEdges.filter(_._1.table == table).map(_._1)
}
