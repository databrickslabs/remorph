package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.intermediate.{UnexpectedNode, TreeNode}
import com.databricks.labs.remorph.transpilers.TranspileException

trait Generator[In <: TreeNode[In], Out] {
  def generate(ctx: GeneratorContext, tree: In): Out
  def unknown(tree: In): TranspileException = TranspileException(UnexpectedNode(tree))
}
