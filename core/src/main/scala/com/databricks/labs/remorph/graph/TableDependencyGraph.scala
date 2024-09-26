package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{QueryHistory, TableDefinition}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.{Result, SourceCode}
import com.typesafe.scalalogging.LazyLogging
import com.databricks.labs.remorph.parsers.{intermediate => ir}

class TableDependencyGraph(parser: PlanParser[_]) extends DependencyGraph with LazyLogging {
  private val nodes = scala.collection.mutable.Set.empty[TableDefinition]
  private val edges = scala.collection.mutable.Set.empty[(TableDefinition, TableDefinition)]
  private val nodeMetadata = scala.collection.mutable.Map.empty[TableDefinition, Map[String, String]]
  private val edgeMetadata = scala.collection.mutable.Map.empty[(TableDefinition, TableDefinition), Map[String, String]]

  override protected def addNode(id: TableDefinition, metadata: Map[String, String]): Unit = {
    nodes += id
    nodeMetadata += id -> metadata
  }

  override protected def addEdge(from: TableDefinition, to: TableDefinition, metadata: Map[String, String]): Unit = {
    edges += ((from, to))
    edgeMetadata += ((from, to)) -> metadata
  }

  override protected def getNodes: Set[TableDefinition] = nodes.toSet

  override protected def getEdges: Set[(TableDefinition, TableDefinition)] = edges.toSet

  def buildGraph(queryHistory: QueryHistory, tableDefinition: Seq[TableDefinition]): Unit = {
    queryHistory.queries.foreach { query =>
      val plan = parser.parse(SourceCode(query.source)).flatMap(parser.visit)

      plan match {
        case Result.Success(plan) =>
          plan collect ({
            case ir.NamedTable(name, _, _) =>
              addNode(tableDefinition.filter(_.table == name).head, Map("query" -> query.source))
            // TODO Add Logic for Edges
            case _ => // Do Nothing
          })

        case _ => logger.warn(s"Failed to produce plan from query: ${query.source}")
      }
    }
  }

  override def getRoot(table: String, level: Int): TableDefinition = getNodes
    .find(_.table == table)
    .getOrElse(throw new NoSuchElementException(s"No table ${table} found"))

  override def getUpstreamTables(table: String): Set[TableDefinition] = getEdges.filter(_._2.table == table).map(_._1)

  override def getDownstreamTables(table: String): Set[TableDefinition] = getEdges.filter(_._1.table == table).map(_._1)
}
