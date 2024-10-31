package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Phase, Transformation, TransformationConstructors, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{TreeNode, UnexpectedNode}

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

}
