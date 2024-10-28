package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.PartialResult
import com.databricks.labs.remorph.generators.Generator
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}

abstract class BasePythonGenerator[In <: TreeNode[In]] extends Generator[In, String] {
  def partialResult(tree: In): Python = partialResult(tree, UnexpectedNode(tree.toString))
  def partialResult(trees: Seq[Any], err: RemorphError): Python =
    PartialResult(s"!!! ${trees.mkString(" | ")} !!!", err)
  def partialResult(tree: Any, err: RemorphError): Python = PartialResult(s"!!! $tree !!!", err)
}
