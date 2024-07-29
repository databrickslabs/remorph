package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.parsers.intermediate.TreeNode
import com.databricks.labs.remorph.transpilers.TranspileException

trait Generator[In <: TreeNode[In], Out] {
  def generate(ctx: GeneratorContext, tree: In): Out
  def unknown(tree: In): TranspileException = TranspileException(s"not implemented: $tree")
}
