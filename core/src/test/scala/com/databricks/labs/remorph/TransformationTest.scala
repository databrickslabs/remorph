package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.{RemorphErrors, UnexpectedNode}
import com.databricks.labs.remorph.preprocessors.jinja.TemplateManager
import com.databricks.labs.remorph.transpilers.Transpiler
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TransformationTest extends AnyWordSpec with Matchers with TransformationConstructors {

  val stubTranspiler = new Transpiler {
    override def transpile(input: PreProcessing): Transformation[String] =
      for {
        _ <- setPhase(Parsing("foo"))
        parsed <- lift(PartialResult("bar", UnexpectedNode("foo")))
        _ <- updatePhase { case p: Parsing => BuildingAst(null, Some(p)) }
        ast <- lift(PartialResult("qux", UnexpectedNode(parsed)))
        _ <- updatePhase { case b: BuildingAst => Optimizing(null, Some(b)) }
        opt <- lift(PartialResult("zaz", UnexpectedNode(ast)))
        _ <- updatePhase { case o: Optimizing => Generating(null, null, null, previousPhase = Some(o)) }
        gen <- lift(PartialResult("nin", UnexpectedNode(opt)))
      } yield gen
  }

  "Transformation" should {
    "collect errors in each phase" in {
      val tm = new TemplateManager()
      stubTranspiler.transpile(PreProcessing("foo")).run(TranspilerState(Init, tm)).map(_._1) shouldBe PartialResult(
        TranspilerState(
          Generating(
            null,
            null,
            null,
            0,
            0,
            Some(Optimizing(
              null,
              Some(BuildingAst(
                null,
                Some(Parsing("foo", "-- test source --", None, List(UnexpectedNode("foo")))),
                List(UnexpectedNode("bar")))),
              List(UnexpectedNode("qux")))),
            List()),
          tm),
        RemorphErrors(List(UnexpectedNode("foo"), UnexpectedNode("bar"), UnexpectedNode("qux"), UnexpectedNode("zaz"))))
    }
  }
}
