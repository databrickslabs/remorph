package com.databricks.labs.remorph.parsers.intermediate

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class CaseInsensitiveCallFunctionSpec extends AnyWordSpec with Matchers {

  "CaseInsensitiveCallFunction" should {

    def matches(cf: CallFunction): Boolean = cf match {
      case CaseInsensitiveCallFunction("FOO", _) => true
      case _ => false
    }

    "match function names in a case insensitive manner" in {
      matches(CallFunction("foo", Seq())) shouldBe true
      matches(CallFunction("FOO", Seq())) shouldBe true
      matches(CallFunction("Foo", Seq())) shouldBe true
      matches(CallFunction("fooo", Seq())) shouldBe false
    }
  }

}
