package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph.{Empty, KoResult, OkResult, PartialResult, RemorphContext, TBAS, WorkflowStage}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SQLInterpolatorSpec extends AnyWordSpec with Matchers with TBAS[RemorphContext] {

  "SQLInterpolator" should {

    "interpolate the empty string" in {
      sql"".runAndDiscardState(Empty) shouldBe OkResult("")
    }

    "interpolate argument-less strings" in {
      sql"foo".runAndDiscardState(Empty) shouldBe OkResult("foo")
    }

    "interpolate argument-less strings with escape sequences" in {
      sql"\tbar\n".runAndDiscardState(Empty) shouldBe OkResult("\tbar\n")
    }

    "interpolate strings consisting only in a single String argument" in {
      val arg = "FOO"
      sql"$arg".runAndDiscardState(Empty) shouldBe OkResult("FOO")
    }

    "interpolate strings consisting only in a single OkResult argument" in {
      val arg = ok("FOO")
      sql"$arg".runAndDiscardState(Empty) shouldBe OkResult("FOO")
    }

    "interpolate strings consisting only in a single argument that is neither String nor OkResult" in {
      val arg = 42
      sql"$arg".runAndDiscardState(Empty) shouldBe OkResult("42")
    }

    "interpolate strings with multiple arguments" in {
      val arg1 = "foo"
      val arg2 = ok("bar")
      val arg3 = 42
      sql"arg1: $arg1, arg2: $arg2, arg3: $arg3".runAndDiscardState(Empty) shouldBe OkResult(
        "arg1: foo, arg2: bar, arg3: 42")
    }

    "accumulate errors when some arguments are PartialResults" in {
      val arg1 = lift(PartialResult("!!! error 1 !!!", UnexpectedNode(Noop.toString)))
      val arg2 = "foo"
      val arg3 = lift(PartialResult("!!! error 2 !!!", UnsupportedDataType(IntegerType.toString)))

      sql"SELECT $arg1 FROM $arg2 WHERE $arg3".runAndDiscardState(Empty) shouldBe PartialResult(
        "SELECT !!! error 1 !!! FROM foo WHERE !!! error 2 !!!",
        RemorphErrors(Seq(UnexpectedNode(Noop.toString), UnsupportedDataType(IntegerType.toString))))
    }

    "return a KoResult if any one of the arguments is a KoResult" in {
      val arg1 = "foo"
      val arg2 = lift(KoResult(WorkflowStage.GENERATE, UnexpectedNode(Noop.toString)))
      val arg3 = 42
      sql"arg1: $arg1, arg2: $arg2, arg3: $arg3".runAndDiscardState(Empty) shouldBe KoResult(
        WorkflowStage.GENERATE,
        UnexpectedNode(Noop.toString))
    }

    "work nicely with mkSql" in {
      val arg1 = "foo"
      val arg2 = lift(PartialResult("!boom!", UnexpectedNode(Noop.toString)))
      val arg3 = 42
      Seq(sql"arg1: $arg1", sql"arg2: $arg2", sql"arg3: $arg3")
        .mkSql(", ")
        .runAndDiscardState(Empty) shouldBe PartialResult(
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
