package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Phase, Transformation, TransformationConstructors, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{TreeNode, UnexpectedNode}

trait Generator[In <: TreeNode[In], Out] extends TransformationConstructors[Phase] {
  def generate(ctx: GeneratorContext, tree: In): Transformation[Phase, Out]
  def unknown(tree: In): Transformation[Phase, Nothing] =
    ko(WorkflowStage.GENERATE, UnexpectedNode(tree.getClass.getSimpleName))
}

trait CodeGenerator[In <: TreeNode[In]] extends Generator[In, String] {

  private def generateAndJoin(
      ctx: GeneratorContext,
      trees: Seq[In],
      separator: String): Transformation[Phase, String] = {
    trees.map(generate(ctx, _)).sequence.map(_.mkString(separator))
  }

  def commas(ctx: GeneratorContext, trees: Seq[In]): Transformation[Phase, String] = generateAndJoin(ctx, trees, ", ")
  def spaces(ctx: GeneratorContext, trees: Seq[In]): Transformation[Phase, String] = generateAndJoin(ctx, trees, " ")

}
