package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.{PartialResult, intermediate => ir}
import com.databricks.labs.remorph.generators.Generator
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}

abstract class BaseSQLGenerator[In <: TreeNode[In]] extends Generator[In, String] {
  def partialResult(tree: In): SQL = partialResult(tree, UnexpectedNode(tree.toString))
  def partialResult(trees: Seq[Any], err: RemorphError): SQL = PartialResult(s"!!! ${trees.mkString(" | ")} !!!", err)
  def partialResult(tree: Any, err: RemorphError): SQL = PartialResult(s"!!! $tree !!!", err)

  /**
   * Generate an inline comment that describes the error that was detected in the unresolved relation,
   * which could be parsing errors, or could be something that is not yet implemented. Implemented as
   * a separate method as we may wish to do more with this in the future.
   */
  protected def describeError(relation: ir.Unresolved[_]): SQL =
    sql"/* The following issues were detected:\n\n   ${relation.message}:\n\n   ${relation.ruleText}\n*/"
}
