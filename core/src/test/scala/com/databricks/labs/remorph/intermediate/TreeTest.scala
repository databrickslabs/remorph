package com.databricks.labs.remorph.intermediate

import org.scalatest.matchers.must.Matchers
import org.scalatest.wordspec.AnyWordSpec

case class TestNode(name: String)(origin: Origin) extends TreeNode[TestNode]()(origin) {
  override def children: Seq[TestNode] = Seq()
}

class TreeTest extends AnyWordSpec with Matchers {
  "TreeNode" should {
    "be equal" in {
      val n1 = TestNode(name = "John")(Origin.empty)
      val n2 = TestNode(name = "John")(Origin(startLine = Some(12)))
      n1 must equal(n2)
    }
  }

}
