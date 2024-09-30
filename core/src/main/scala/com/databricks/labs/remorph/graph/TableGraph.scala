package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory, TableDefinition}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.{Result, SourceCode}
import com.typesafe.scalalogging.LazyLogging
import com.databricks.labs.remorph.parsers.{intermediate => ir}

protected case class Node(tableDefinition: TableDefinition, metadata: Map[String, Set[String]])
protected case class Edge(from: TableDefinition, to: Option[TableDefinition], metadata: Map[String, String])

class TableGraph(parser: PlanParser[_]) extends DependencyGraph with LazyLogging {
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

  override protected def addEdge(from: TableDefinition, to: Option[TableDefinition],
                                 metadata: Map[String, String]): Unit = {
    edges += Edge(from, to, metadata)
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
        case Some(name) => addNode(name, Map("query" -> query.id))
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
      val plan = parser.parse(SourceCode(query.source)).flatMap(parser.visit)
      plan match {
        case Result.Failure(_, errorJson) =>
          logger.warn(s"Failed to produce plan from query: ${query.source}")
          logger.debug(s"Error: $errorJson")
        case Result.Success(p) =>
          buildNode(p, tableDefinition, query)
          generateEdges(p, tableDefinition, query.id)
      }
        } catch {
        // TODO Null Pointer Exception is thrown as Result.Success, need to investigate for Merge Query.
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
        inDegreeMap(toTable) += 1
      }
    }
    inDegreeMap.toMap
  }

  // TODO Implement logic for fetching edges(parents) only upto certain level
  def getRootTables(): Set[TableDefinition] = {
    val inDegreeMap = countInDegrees()
    nodes.map(_.tableDefinition)
      .filter(table => inDegreeMap.getOrElse(table, 0) == 0)
      .toSet
  }


  override def getUpstreamTables(table: TableDefinition): Set[TableDefinition] = {
    edges.filter(_.to.contains(table)).map(_.from).toSet
  }

  override def getDownstreamTables(table: TableDefinition): Set[TableDefinition] = {
    edges.filter(_.from == table).flatMap(_.to).toSet
  }
}
