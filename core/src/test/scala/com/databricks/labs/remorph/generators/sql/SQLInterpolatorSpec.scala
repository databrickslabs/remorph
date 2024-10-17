package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.intermediate.{Noop, UnexpectedNode}
import com.databricks.labs.remorph.{Failure, Success, WorkflowStage}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SQLInterpolatorSpec extends AnyWordSpec with Matchers {

  "SQLInterpolator" should {

    "interpolate the empty string" in {
      sql"" shouldBe Success("")
    }

    "interpolate argument-less strings" in {
      sql"foo" shouldBe Success("foo")
    }

    "interpolate argument-less strings with escape sequences" in {
      sql"\tbar\n" shouldBe Success("\tbar\n")
    }

    "interpolate strings consisting only in a single String argument" in {
      val arg = "FOO"
      sql"$arg" shouldBe Success("FOO")
    }

    "interpolate strings consisting only in a single Success argument" in {
      val arg = Success("FOO")
      sql"$arg" shouldBe Success("FOO")
    }

    "interpolate strings consisting only in a single argument that is neither String nor Success" in {
      val arg = 42
      sql"$arg" shouldBe Success("42")
    }

    "interpolate strings with multiple arguments" in {
      val arg1 = "foo"
      val arg2 = Success("bar")
      val arg3 = 42
      sql"arg1: $arg1, arg2: $arg2, arg3: $arg3" shouldBe Success("arg1: foo, arg2: bar, arg3: 42")
    }

    "return a Failure if any one of the arguments is a Failure" in {
      val arg1 = "foo"
      val arg2 = Failure(WorkflowStage.GENERATE, UnexpectedNode(Noop))
      val arg3 = 42
      sql"arg1: $arg1, arg2: $arg2, arg3: $arg3" shouldBe Failure(WorkflowStage.GENERATE, UnexpectedNode(Noop))
    }

    "unfortunately, if evaluating one of the arguments throws an exception, " +
      "it cannot be caught by the interpolator because arguments are evaluated eagerly" in {
        def boom(): Unit = throw new RuntimeException("boom")
        a[RuntimeException] should be thrownBy sql"3...2...1...${boom()}"
      }
  }
}
