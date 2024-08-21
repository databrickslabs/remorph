package com.databricks.labs.remorph
import scala.collection.mutable

case object Action extends Enumeration {
  type Operation = Value
  val Read, Write, Update, Delete = Value
}

case class Node(name: String)

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

  def getNodes: Set[Node] = nodes.toSet

  def getEdges: Set[Edge] = edges.toSet

  def getImmediateParents(node: Node): Set[Node] = {
    edges.filter(_.to == node).map(_.from).toSet
  }
}
