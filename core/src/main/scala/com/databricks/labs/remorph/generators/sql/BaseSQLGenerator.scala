package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.PartialResult
import com.databricks.labs.remorph.generators.Generator
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}

abstract class BaseSQLGenerator[In <: TreeNode[In]] extends Generator[In, String] {
  def partialResult(tree: In): SQL = partialResult(tree, UnexpectedNode(tree.toString))
  def partialResult(trees: Seq[Any], err: RemorphError): SQL = PartialResult(s"!!! ${trees.mkString(" | ")} !!!", err)
  def partialResult(tree: Any, err: RemorphError): SQL = PartialResult(s"!!! $tree !!!", err)
}
