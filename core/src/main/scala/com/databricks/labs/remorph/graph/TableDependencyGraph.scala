package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory, TableDefinition}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.{Result, SourceCode}
import com.typesafe.scalalogging.LazyLogging
import com.databricks.labs.remorph.parsers.{intermediate => ir}

protected case class Node(tableDefinition: TableDefinition, metadata: Map[String, Set[String]])
protected case class Edge(from: TableDefinition, to: TableDefinition, metadata: Map[String, String])

class TableDependencyGraph(parser: PlanParser[_]) extends DependencyGraph with LazyLogging {
  val nodes = scala.collection.mutable.Set.empty[Node]
  val edges = scala.collection.mutable.Set.empty[Edge]

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

  private def getTableName(plan: ir.LogicalPlan): String = {
    plan collectFirst { case x: ir.NamedTable =>
      x.unparsed_identifier
    }
  }.getOrElse("None")

  private def generateEdges(plan: ir.LogicalPlan, tableDefinition: Seq[TableDefinition], queryId: String): Unit = {
    var toTable: TableDefinition = null
    var action = "SELECT"
    var fromTable: Seq[TableDefinition] = Seq.empty

    def collectTables(node: ir.LogicalPlan): Unit = {
      node match {
        case _: ir.CreateTable =>
          toTable = tableDefinition.filter(_.table == getTableName(plan)).head
          action = "CREATE"
        case _: ir.InsertIntoTable =>
          toTable = tableDefinition.filter(_.table == getTableName(plan)).head
          action = "INSERT"
        case _: ir.DeleteFromTable =>
          toTable = tableDefinition.filter(_.table == getTableName(plan)).head
          action = "DELETE"
        case _: ir.UpdateTable =>
          toTable = tableDefinition.filter(_.table == getTableName(plan)).head
          action = "UPDATE"
        case _: ir.MergeIntoTable =>
          toTable = tableDefinition.filter(_.table == getTableName(plan)).head
          action = "MERGE"
        case _: ir.Project | _: ir.Join | _: ir.SubqueryAlias | _: ir.Filter =>
          val tableList = plan collect { case x: ir.NamedTable =>
            x.unparsed_identifier
          }
          fromTable = tableDefinition.filter(x => tableList.contains(x.table))
        case _ => // Do nothing
      }
      node.children.foreach(collectTables)
    }

    collectTables(plan)

    if (fromTable.isEmpty) {
      logger.warn(s"No tables found for insert into table values query")
    } else {
      fromTable.foreach(f => {
        if (f != toTable) {
          addEdge(f, toTable, Map("query" -> queryId, "action" -> action))
        } else {
          logger.warn(s"Ignoring reference detected for table ${f.table}")
        }
      })
    }
  }

  private def buildNode(plan: ir.LogicalPlan, tableDefinition: Seq[TableDefinition], query: ExecutedQuery): Unit = {
    plan collect { case x: ir.NamedTable =>
      print(x.unparsed_identifier)
      print("\n")
      tableDefinition.find(_.table == x.unparsed_identifier) match {
        case Some(name) => addNode(name, Map("query" -> query.id))
        case None =>
          logger.warn(
            s"Table ${x.unparsed_identifier} not found in table definitions " +
              s"or is it a subquery alias")
      }
    }
  }

  def buildDependency(queryHistory: QueryHistory, tableDefinition: Seq[TableDefinition]): Unit = {
    queryHistory.queries.foreach { query =>
      print("\n")
      print(query.source)
      print("\n")
      val plan = parser.parse(SourceCode(query.source)).flatMap(parser.visit)
      plan match {
        case Result.Success(p) => buildNode(p, tableDefinition, query)
          generateEdges(p, tableDefinition, query.id)
        case _ => logger.warn(s"Failed to produce plan from query: ${query.source}")
      }
    }
  }

  // TODO Implement logic for fetching edges(parents) only upto certain level
  override def getRoot(table: String, level: Int = 1): TableDefinition = {
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
    findRoot(targetNode, level).tableDefinition
  }

  override def getUpstreamTables(table: String): Set[TableDefinition] = Set.empty[TableDefinition]

  override def getDownstreamTables(table: String): Set[TableDefinition] = Set.empty[TableDefinition]
}
