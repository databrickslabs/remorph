package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.intermediate.{IntegerType, Noop, RemorphErrors, UnexpectedNode, UnsupportedDataType}
import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult, WorkflowStage}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SQLInterpolatorSpec extends AnyWordSpec with Matchers {

  "SQLInterpolator" should {

    "interpolate the empty string" in {
      sql"" shouldBe OkResult("")
    }

    "interpolate argument-less strings" in {
      sql"foo" shouldBe OkResult("foo")
    }

    "interpolate argument-less strings with escape sequences" in {
      sql"\tbar\n" shouldBe OkResult("\tbar\n")
    }

    "interpolate strings consisting only in a single String argument" in {
      val arg = "FOO"
      sql"$arg" shouldBe OkResult("FOO")
    }

    "interpolate strings consisting only in a single OkResult argument" in {
      val arg = OkResult("FOO")
      sql"$arg" shouldBe OkResult("FOO")
    }

    "interpolate strings consisting only in a single argument that is neither String nor OkResult" in {
      val arg = 42
      sql"$arg" shouldBe OkResult("42")
    }

    "interpolate strings with multiple arguments" in {
      val arg1 = "foo"
      val arg2 = OkResult("bar")
      val arg3 = 42
      sql"arg1: $arg1, arg2: $arg2, arg3: $arg3" shouldBe OkResult("arg1: foo, arg2: bar, arg3: 42")
    }

    "accumulate errors when some arguments are PartialResults" in {
      val arg1 = PartialResult("!!! error 1 !!!", UnexpectedNode(Noop))
      val arg2 = "foo"
      val arg3 = PartialResult("!!! error 2 !!!", UnsupportedDataType(IntegerType))

      sql"SELECT $arg1 FROM $arg2 WHERE $arg3" shouldBe PartialResult(
        "SELECT !!! error 1 !!! FROM foo WHERE !!! error 2 !!!",
        RemorphErrors(Seq(UnexpectedNode(Noop), UnsupportedDataType(IntegerType))))
    }

    "return a KoResult if any one of the arguments is a KoResult" in {
      val arg1 = "foo"
      val arg2 = KoResult(WorkflowStage.GENERATE, UnexpectedNode(Noop))
      val arg3 = 42
      sql"arg1: $arg1, arg2: $arg2, arg3: $arg3" shouldBe KoResult(WorkflowStage.GENERATE, UnexpectedNode(Noop))
    }

    "work nicely with mkSql" in {
      val arg1 = "foo"
      val arg2 = PartialResult("!boom!", UnexpectedNode(Noop.toString))
      val arg3 = 42
      Seq(sql"arg1: $arg1", sql"arg2: $arg2", sql"arg3: $arg3").mkSql(", ") shouldBe PartialResult(
        "arg1: foo, arg2: !boom!, arg3: 42",
        UnexpectedNode(Noop.toString))
    }

    "unfortunately, if evaluating one of the arguments throws an exception, " +
      "it cannot be caught by the interpolator because arguments are evaluated eagerly" in {
        def boom(): Unit = throw new RuntimeException("boom")
        a[RuntimeException] should be thrownBy sql"3...2...1...${boom()}"
      }
  }
}
