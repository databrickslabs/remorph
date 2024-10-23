package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{RemorphContext, TBA, TBAS, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{TreeNode, UnexpectedNode}

trait Generator[In <: TreeNode[In], Out] extends TBAS[RemorphContext] {
  def generate(ctx: GeneratorContext, tree: In): TBA[RemorphContext, Out]
  def unknown(tree: In): TBA[RemorphContext, Nothing] =
    ko(WorkflowStage.GENERATE, UnexpectedNode(tree.getClass.getSimpleName))
}
