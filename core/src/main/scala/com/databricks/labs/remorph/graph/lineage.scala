package com.databricks.labs.remorph.graph

import scala.collection.mutable

case object Action extends Enumeration {
  type Operation = Value
  val Read, Write, Update, Delete, Merge = Value
}

case class Node(catalog: Option[String], schema: String, table: String)

case class Edge(from: Node, operator: Action.Operation, to: Node)

class Lineage {
  private val nodes: mutable.Set[Node] = mutable.Set()
  private val edges: mutable.Set[Edge] = mutable.Set()

  def addNode(node: Node): Unit = {
    nodes += node
  }

  def addEdge(from: Node, to: Node, operator: Action.Operation): Unit = {
    if (edges.exists(e => e.from == to && e.to == from)) {
      throw new IllegalArgumentException("Adding this edge would create a cycle")
    }
    edges += Edge(from, operator, to)
  }

  private def getNodes: Seq[Node] = nodes.toSeq

  private def getEdges: Set[Edge] = edges.toSet

  def getImmediateParents(node: String): Set[Node] = {
    // Update table will have the same parent and child name
    getEdges.filter(x => x.to != x.from && x.to.table == node).map(_.from)
  }

  def roots: Set[Node] = nodes.filter(n => edges.forall(e => e.to != n)).toSet

  def sorted: Set[Node] = getNodes.sortBy(n => n.table).toSet
}
