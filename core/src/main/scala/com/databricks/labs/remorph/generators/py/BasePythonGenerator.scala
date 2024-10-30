package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.PartialResult
import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}

abstract class BasePythonGenerator[In <: TreeNode[In]] extends Generator[In, String] {
  def commas(ctx: GeneratorContext, nodes: Seq[In]): Python = nodes.map(generate(ctx, _)).mkTba(", ")

  def partialResult(tree: In): Python = partialResult(tree, UnexpectedNode(tree.toString))
  def partialResult(trees: Seq[Any], err: RemorphError): Python =
    lift(PartialResult(s"# FIXME: ${trees.mkString(" | ")} !!!", err))
  def partialResult(tree: Any, err: RemorphError): Python = lift(PartialResult(s"# FIXME: $tree !!!", err))
}
