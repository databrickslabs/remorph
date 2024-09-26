package com.databricks.labs.remorph.graph

import com.databricks.labs.remorph.discovery.TableDefinition

trait DependencyGraph {
  protected def addNode(id: TableDefinition, metadata: Map[String, String]): Unit
  protected def addEdge(from: TableDefinition, to: TableDefinition, metadata: Map[String, String]): Unit
  protected def getNodes: Set[TableDefinition]
  protected def getEdges: Set[(TableDefinition, TableDefinition)]
  def getUpstreamTables(table: String): Set[TableDefinition]
  def getDownstreamTables(table: String): Set[TableDefinition]
  def getRoot(table: String, level: Int): TableDefinition
}
