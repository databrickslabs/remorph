package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.{RemorphErrors, UnexpectedNode}
import com.databricks.labs.remorph.transpilers.Transpiler
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TransformationTest extends AnyWordSpec with Matchers with TransformationConstructors {

  val stubTranspiler = new Transpiler {
    override def transpile(input: Parsing): Transformation[String] =
      for {
        _ <- set(Parsing("foo"))
        parsed <- lift(PartialResult("bar", UnexpectedNode("foo")))
        _ <- update { case p: Parsing => BuildingAst(null, Some(p)) }
        ast <- lift(PartialResult("qux", UnexpectedNode(parsed)))
        _ <- update { case b: BuildingAst => Optimizing(null, Some(b)) }
        opt <- lift(PartialResult("zaz", UnexpectedNode(ast)))
        _ <- update { case o: Optimizing => Generating(null, null, null, previousPhase = Some(o)) }
        gen <- lift(PartialResult("nin", UnexpectedNode(opt)))
      } yield gen
  }

  "Transformation" should {
    "collect errors in each phase" in {
      stubTranspiler.transpile(Parsing("foo")).run(Init).map(_._1) shouldBe PartialResult(
        Generating(
          null,
          null,
          null,
          0,
          0,
          Some(
            Optimizing(
              null,
              Some(
                BuildingAst(
                  null,
                  Some(Parsing("foo", "-- test source --", List(UnexpectedNode("foo")))),
                  List(UnexpectedNode("bar")))),
              List(UnexpectedNode("qux")))),
          List()),
        RemorphErrors(List(UnexpectedNode("foo"), UnexpectedNode("bar"), UnexpectedNode("qux"), UnexpectedNode("zaz"))))
    }
  }
}
