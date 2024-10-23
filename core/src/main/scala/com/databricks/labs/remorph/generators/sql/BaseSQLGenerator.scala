package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.{PartialResult, RemorphContext, TBA}
import com.databricks.labs.remorph.generators.Generator
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}

abstract class BaseSQLGenerator[In <: TreeNode[In]] extends Generator[In, String] {
  def partialResult(tree: In): TBA[RemorphContext, String] = partialResult(tree, UnexpectedNode(tree.toString))
  def partialResult(trees: Seq[Any], err: RemorphError): TBA[RemorphContext, String] = lift(
    PartialResult(s"!!! ${trees.mkString(" | ")} !!!", err))
  def partialResult(tree: Any, err: RemorphError): TBA[RemorphContext, String] = lift(
    PartialResult(s"!!! $tree !!!", err))
}
