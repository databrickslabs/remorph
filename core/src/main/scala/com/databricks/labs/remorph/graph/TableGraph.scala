package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory, TableDefinition}
import com.databricks.labs.remorph.parsers.PlanParser
import com.typesafe.scalalogging.LazyLogging
import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult, Parsing, intermediate => ir}

protected case class Node(tableDefinition: TableDefinition, metadata: Map[String, Set[String]])
// `from` is the table which is sourced to create `to` table
protected case class Edge(from: Node, to: Option[Node], metadata: Map[String, String])

class TableGraph(parser: PlanParser[_]) extends DependencyGraph with LazyLogging {
  private val nodes = scala.collection.mutable.Set.empty[Node]
  private val edges = scala.collection.mutable.Set.empty[Edge]

  override protected def addNode(id: TableDefinition, metadata: Map[String, Set[String]]): Unit = {
    // Metadata list of query ids and add node only if it is not already present.
    // for Example if a table is used in multiple queries, we need to consolidate the metadata
    // here we are storing only query hash id as metadata not the query itself
    val existingNode = nodes.find(_.tableDefinition == id)
    existingNode match {
      case Some(node) =>
        val consolidatedMetadata = (node.metadata.toSeq ++ metadata.toSeq)
          .groupBy(_._1)
          .mapValues(_.flatten(_._2).toSet)
        nodes -= node
        nodes += node.copy(metadata = consolidatedMetadata)
      case None =>
        nodes += Node(id, metadata)
    }
  }

  override protected def addEdge(
      from: TableDefinition,
      to: Option[TableDefinition],
      metadata: Map[String, String]): Unit = {
    val fromNode = nodes.find(_.tableDefinition == from).get
    val toNode = to.flatMap(td => nodes.find(_.tableDefinition == td))
    edges += Edge(fromNode, toNode, metadata)
  }

  private def getTableName(plan: ir.LogicalPlan): String = {
    plan collectFirst { case x: ir.NamedTable =>
      x.unparsed_identifier
    }
  }.getOrElse("None")

  private def generateEdges(plan: ir.LogicalPlan, tableDefinition: Set[TableDefinition], queryId: String): Unit = {
    var toTable: Option[TableDefinition] = None
    var action = "SELECT"
    var fromTable: Seq[TableDefinition] = Seq.empty

    def collectTables(node: ir.LogicalPlan): Unit = {
      node match {
        case _: ir.CreateTable =>
          toTable = Some(tableDefinition.filter(_.table == getTableName(plan)).head)
          action = "CREATE"
        case _: ir.InsertIntoTable =>
          toTable = Some(tableDefinition.filter(_.table == getTableName(plan)).head)
          action = "INSERT"
        case _: ir.DeleteFromTable =>
          toTable = Some(tableDefinition.filter(_.table == getTableName(plan)).head)
          action = "DELETE"
        case _: ir.UpdateTable =>
          toTable = Some(tableDefinition.filter(_.table == getTableName(plan)).head)
          action = "UPDATE"
        case _: ir.MergeIntoTable =>
          toTable = Some(tableDefinition.filter(_.table == getTableName(plan)).head)
          action = "MERGE"
        case _: ir.Project | _: ir.Join | _: ir.SubqueryAlias | _: ir.Filter =>
          val tableList = plan collect { case x: ir.NamedTable =>
            x.unparsed_identifier
          }
          fromTable = tableDefinition.toSeq.filter(x => tableList.contains(x.table))
        case _ => // Do nothing
      }
      node.children.foreach(collectTables)
    }

    collectTables(plan)

    if (fromTable.nonEmpty) {
      fromTable.foreach(f => {
        if (toTable.isDefined && f != toTable.get) {
          addEdge(f, toTable, Map("query" -> queryId, "action" -> action))
        } else {
          logger.debug(s"Ignoring reference detected for table ${f.table}")
        }
      })
    } else {
      logger.debug(s"No tables found for insert into table values query")
    }
  }

  private def buildNode(plan: ir.LogicalPlan, tableDefinition: Set[TableDefinition], query: ExecutedQuery): Unit = {
    plan collect { case x: ir.NamedTable =>
      tableDefinition.find(_.table == x.unparsed_identifier) match {
        case Some(name) => addNode(name, Map("query" -> Set(query.id)))
        case None =>
          logger.warn(
            s"Table ${x.unparsed_identifier} not found in table definitions " +
              s"or is it a subquery alias")
      }
    }
  }

  def buildDependency(queryHistory: QueryHistory, tableDefinition: Set[TableDefinition]): Unit = {
    queryHistory.queries.foreach { query =>
      try {
        val plan = parser.parse(Parsing(query.source)).flatMap(parser.visit).run(Parsing(query.source))
        plan match {
          case KoResult(_, error) =>
            logger.warn(s"Failed to produce plan from query: ${query.id}")
            logger.debug(s"Error: ${error.msg}")
          case PartialResult((_, p), error) =>
            logger.warn(s"Errors occurred while producing plan from query ${query.id}")
            logger.debug(s"Error: ${error.msg}")
            buildNode(p, tableDefinition, query)
            generateEdges(p, tableDefinition, query.id)
          case OkResult((_, p)) =>
            buildNode(p, tableDefinition, query)
            generateEdges(p, tableDefinition, query.id)
        }
      } catch {
        // TODO Null Pointer Exception is thrown as OkResult, need to investigate for Merge Query.
        case e: Exception => logger.warn(s"Failed to produce plan from query: ${query.source}")
      }
    }
  }

  private def countInDegrees(): Map[TableDefinition, Int] = {
    val inDegreeMap = scala.collection.mutable.Map[TableDefinition, Int]().withDefaultValue(0)

    // Initialize inDegreeMap with all nodes
    nodes.foreach { node =>
      inDegreeMap(node.tableDefinition) = 0
    }

    edges.foreach { edge =>
      edge.to.foreach { toTable =>
        inDegreeMap(toTable.tableDefinition) += 1
      }
    }
    inDegreeMap.toMap
  }

  // TODO Implement logic for fetching edges(parents) only upto certain level
  def getRootTables(): Set[TableDefinition] = {
    val inDegreeMap = countInDegrees()
    nodes
      .map(_.tableDefinition)
      .filter(table => inDegreeMap.getOrElse(table, 0) == 0)
      .toSet
  }

  override def getUpstreamTables(table: TableDefinition): Set[TableDefinition] = {
    def getUpstreamTablesRec(node: Node, visited: Set[Node]): Set[TableDefinition] = {
      if (visited.contains(node)) {
        Set.empty
      } else {
        val parents = edges.filter(_.to.get.tableDefinition == node.tableDefinition).map(_.from).toSet
        parents.flatMap(parent => getUpstreamTablesRec(parent, visited + node)) + node.tableDefinition
      }
    }

    nodes.find(_.tableDefinition == table) match {
      case Some(n) => getUpstreamTablesRec(n, Set.empty) - table
      case None =>
        logger.warn(s"Table ${table.table} not found in the graph")
        Set.empty[TableDefinition]
    }
  }

  override def getDownstreamTables(table: TableDefinition): Set[TableDefinition] = {
    def getDownstreamTablesRec(node: Node, visited: Set[Node]): Set[TableDefinition] = {
      if (visited.contains(node)) {
        Set.empty
      } else {
        val children = edges.filter(_.from.tableDefinition == node.tableDefinition).flatMap(_.to).toSet
        children.flatMap(child => getDownstreamTablesRec(child, visited + node)) + node.tableDefinition
      }
    }
    nodes.find(_.tableDefinition == table) match {
      case Some(n) =>
        getDownstreamTablesRec(n, Set.empty) - table
      case None =>
        logger.warn(s"Table ${table.table} not found in the graph")
        Set.empty[TableDefinition]
    }
  }
}
