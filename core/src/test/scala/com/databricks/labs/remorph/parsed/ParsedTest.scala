package com.databricks.labs.remorph.parsed

import com.databricks.labs.remorph.intermediate.LineCommentNode
import org.scalatest.matchers.must.Matchers
import org.scalatest.wordspec.AnyWordSpec

class ParsedTest extends AnyWordSpec with Matchers {

  "ParsedNode" should {
    "have same hashCode" in {
      val comment = LineCommentNode("John")
      val parsed = new ParsedNode[LineCommentNode](comment, ParsedRange.empty)
      comment.hashCode() must equal(parsed.hashCode())
    }
    "be equal" in {
      val c1 = LineCommentNode("John")
      val n1 = new ParsedNode[LineCommentNode](c1, ParsedRange.empty)
      val c2 = LineCommentNode("John")
      val range = ParsedRange(ParsedLocation(12, 2, 3), ParsedLocation(13, 9, 7))
      val n2 = new ParsedNode[LineCommentNode](c2, range)
      c1 must equal(c2)
      n1 must equal(n2)
    }
  }

}
