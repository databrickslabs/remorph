package com.databricks.labs.remorph.intermediate

import org.scalatest.matchers.must.Matchers
import org.scalatest.wordspec.AnyWordSpec

class JoinTest extends AnyWordSpec with Matchers {
  "Join" should {
    "propagage expressions" in {
      val join = Join(
        NoopNode,
        NoopNode,
        Some(Name("foo")),
        InnerJoin,
        Seq.empty,
        JoinDataType(is_left_struct = true, is_right_struct = true))
      join.expressions mustBe Seq(Name("foo"))
    }
  }
}
