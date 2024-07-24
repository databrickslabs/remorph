package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.parsers.intermediate.TreeNode

trait Generator[In <: TreeNode[In], Out] {
  def generate(ctx: GeneratorContext, tree: In): Out
}
