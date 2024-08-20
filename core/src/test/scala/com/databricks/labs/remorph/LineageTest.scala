package com.databricks.labs.remorph

import org.scalatest.funsuite.AnyFunSuite

class LineageTest extends AnyFunSuite {

  test("addNode should add a node to the DAG") {
    val dag = new Lineage
    val node = Node("A")
    dag.addNode(node)
    assert(dag.getNodes.contains(node))
  }

  test("addEdge should add an edge to the DAG") {
    val dag = new Lineage
    val nodeA = Node("A")
    val nodeB = Node("B")
    dag.addNode(nodeA)
    dag.addNode(nodeB)
    dag.addEdge(nodeA, nodeB, Action.Read)
    assert(dag.getEdges.contains(Edge(nodeA, Action.Read, nodeB)))
  }

  test("addEdge should throw an exception if adding an edge creates a cycle") {
    val dag = new Lineage
    val nodeA = Node("A")
    val nodeB = Node("B")
    dag.addNode(nodeA)
    dag.addNode(nodeB)
    dag.addEdge(nodeA, nodeB, Action.Write)
    assertThrows[IllegalArgumentException] {
      dag.addEdge(nodeB, nodeA, Action.Write)
    }
  }

  test("getImmediateParents should return the immediate parents of a node") {
    val dag = new Lineage
    val nodeA = Node("A")
    val nodeB = Node("B")
    val nodeC = Node("C")
    dag.addNode(nodeA)
    dag.addNode(nodeB)
    dag.addNode(nodeC)
    dag.addEdge(nodeA, nodeB, Action.Read)
    dag.addEdge(nodeC, nodeB, Action.Read)
    assert(dag.getImmediateParents(nodeB) == Set(nodeA, nodeC))
  }
}
