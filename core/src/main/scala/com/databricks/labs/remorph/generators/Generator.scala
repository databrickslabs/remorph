package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{KoResult, Result, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{TreeNode, UnexpectedNode}

trait Generator[In <: TreeNode[In], Out] {
  def generate(ctx: GeneratorContext, tree: In): Result[Out]
  def unknown(tree: In): Result[Out] =
    KoResult(WorkflowStage.GENERATE, UnexpectedNode(tree.getClass.getSimpleName))
}
