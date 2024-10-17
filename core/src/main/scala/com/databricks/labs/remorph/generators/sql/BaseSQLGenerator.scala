package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.PartialResult
import com.databricks.labs.remorph.generators.Generator
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}

abstract class BaseSQLGenerator[In <: TreeNode[In]] extends Generator[In, String] {
  def partialResult(tree: In): SQL = partialResult(tree, UnexpectedNode(tree))
  def partialResult(tree: In, err: RemorphError): SQL = PartialResult(s"!!! $tree !!!", err)
}
