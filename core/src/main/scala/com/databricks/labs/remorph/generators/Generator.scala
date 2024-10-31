package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Generating, KoResult, OkResult, Phase, Transformation, TransformationConstructors, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{IncoherentState, TreeNode, UnexpectedNode}

trait Generator[In <: TreeNode[In], Out] extends TransformationConstructors[Phase] {
  def generate(tree: In): Transformation[Phase, Out]
  def unknown(tree: In): Transformation[Phase, Nothing] =
    ko(WorkflowStage.GENERATE, UnexpectedNode(tree.getClass.getSimpleName))
}

trait CodeGenerator[In <: TreeNode[In]] extends Generator[In, String] {

  private def generateAndJoin(trees: Seq[In], separator: String): Transformation[Phase, String] = {
    trees.map(generate).sequence.map(_.mkString(separator))
  }

  def commas(trees: Seq[In]): Transformation[Phase, String] = generateAndJoin(trees, ", ")
  def spaces(trees: Seq[In]): Transformation[Phase, String] = generateAndJoin(trees, " ")

  def updateGenCtx(f: GeneratorContext => GeneratorContext): Transformation[Phase, Unit] = new Transformation(OkResult {
    case g: Generating => OkResult((g.copy(ctx = f(g.ctx)), ()))
    case p => KoResult(WorkflowStage.GENERATE, IncoherentState(p, classOf[Generating]))
  })

  def nest: Transformation[Phase, Unit] = updateGenCtx(_.nest)

  def unnest: Transformation[Phase, Unit] = updateGenCtx(_.unnest)

  def withIndentedBlock(
      header: Transformation[Phase, String],
      body: Transformation[Phase, String]): Transformation[Phase, String] =
    for {
      h <- header
      _ <- nest
      b <- body
      _ <- unnest
    } yield h + "\n" + b

  def withGenCtx(transformation: GeneratorContext => Transformation[Phase, String]): Transformation[Phase, String] =
    new Transformation[Phase, GeneratorContext](OkResult {
      case g: Generating => OkResult((g, g.ctx))
      case p => KoResult(WorkflowStage.GENERATE, IncoherentState(p, classOf[Generating]))
    }).flatMap(transformation)
}
