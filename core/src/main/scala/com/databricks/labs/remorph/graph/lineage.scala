package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.TableDefinition

trait DependencyGraph {
  protected def addNode(id: TableDefinition, metadata: Map[String, Set[String]]): Unit
  protected def addEdge(from: TableDefinition, to: Option[TableDefinition], metadata: Map[String, String]): Unit
  def getUpstreamTables(table: TableDefinition): Set[TableDefinition]
  def getDownstreamTables(table: TableDefinition): Set[TableDefinition]
}
