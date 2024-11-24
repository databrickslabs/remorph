package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class CodeInterpolatorSpec extends AnyWordSpec with Matchers with TransformationConstructors {

  "SQLInterpolator" should {

    "interpolate the empty string" in {
      code"".runAndDiscardState(Init) shouldBe OkResult("")
    }

    "interpolate argument-less strings" in {
      code"foo".runAndDiscardState(Init) shouldBe OkResult("foo")
    }

    "interpolate argument-less strings with escape sequences" in {
      code"\tbar\n".runAndDiscardState(Init) shouldBe OkResult("\tbar\n")
    }

    "interpolate strings consisting only in a single String argument" in {
      val arg = "FOO"
      code"$arg".runAndDiscardState(Init) shouldBe OkResult("FOO")
    }

    "interpolate strings consisting only in a single OkResult argument" in {
      val arg = ok("FOO")
      code"$arg".runAndDiscardState(Init) shouldBe OkResult("FOO")
    }

    "interpolate strings consisting only in a single argument that is neither String nor OkResult" in {
      val arg = 42
      code"$arg".runAndDiscardState(Init) shouldBe OkResult("42")
    }

    "interpolate strings with multiple arguments" in {
      val arg1 = "foo"
      val arg2 = ok("bar")
      val arg3 = 42
      code"arg1: $arg1, arg2: $arg2, arg3: $arg3".runAndDiscardState(Init) shouldBe OkResult(
        "arg1: foo, arg2: bar, arg3: 42")
    }

    "accumulate errors when some arguments are PartialResults" in {
      val arg1 = lift(PartialResult("!!! error 1 !!!", UnexpectedNode(Noop.toString)))
      val arg2 = "foo"
      val arg3 = lift(PartialResult("!!! error 2 !!!", UnsupportedDataType(IntegerType.toString)))

      code"SELECT $arg1 FROM $arg2 WHERE $arg3".runAndDiscardState(Init) shouldBe PartialResult(
        "SELECT !!! error 1 !!! FROM foo WHERE !!! error 2 !!!",
        RemorphErrors(Seq(UnexpectedNode(Noop.toString), UnsupportedDataType(IntegerType.toString))))
    }

    "return a KoResult if any one of the arguments is a KoResult" in {
      val arg1 = "foo"
      val arg2 = lift(KoResult(WorkflowStage.GENERATE, UnexpectedNode(Noop.toString)))
      val arg3 = 42
      code"arg1: $arg1, arg2: $arg2, arg3: $arg3".runAndDiscardState(Init) shouldBe KoResult(
        WorkflowStage.GENERATE,
        UnexpectedNode(Noop.toString))
    }

    "work nicely with mkTba" in {
      val arg1 = "foo"
      val arg2 = lift(PartialResult("!boom!", UnexpectedNode(Noop.toString)))
      val arg3 = 42
      Seq(code"arg1: $arg1", code"arg2: $arg2", code"arg3: $arg3")
        .mkCode(", ")
        .runAndDiscardState(Init) shouldBe PartialResult(
        "arg1: foo, arg2: !boom!, arg3: 42",
        UnexpectedNode(Noop.toString))
    }

    "unfortunately, if evaluating one of the arguments throws an exception, " +
      "it cannot be caught by the interpolator because arguments are evaluated eagerly" in {
        def boom(): Unit = throw new RuntimeException("boom")
        val three = ok("3")
        val two = ok("2")
        val one = ok("1")
        val aftermath = ok("everything exploded")
        a[RuntimeException] should be thrownBy code"$three...$two...$one...${boom()}...$aftermath"
      }

    "wrap 'normal' exception, such as invalid escapes, in a failure" in {
      code"\D".runAndDiscardState(Init) shouldBe an[KoResult]
    }

    "foo" in {
      val foo = RemorphError
      println(foo)
      succeed
    }
  }
}
