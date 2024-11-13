package com.databricks.labs.remorph.intermediate

import org.scalatest.matchers.must.Matchers
import org.scalatest.wordspec.AnyWordSpec

case class TestNode(name: String)(origin: Option[Origin]) extends TreeNode[TestNode](origin) {
  override def children: Seq[TestNode] = Seq()
}

class TreeTest extends AnyWordSpec with Matchers {
  "TreeNode" should {
    "be equal" in {
      val n1 = TestNode(name = "John")(Option.empty)
      val n2 = TestNode(name = "John")(
        Some(
          Origin(startLine = 12, startColumn = 2, startTokenIndex = 3, endLine = 13, endColumn = 9, endTokenIndex = 7)))
      n1 must equal(n2)
    }
  }

}
