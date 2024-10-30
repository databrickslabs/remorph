package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.intermediate.{RemorphError, TreeNode, UnexpectedNode}
import com.databricks.labs.remorph.{PartialResult, intermediate => ir}

abstract class BaseSQLGenerator[In <: TreeNode[In]] extends CodeGenerator[In] {
  def partialResult(tree: In): SQL = partialResult(tree, UnexpectedNode(tree.toString))
  def partialResult(trees: Seq[Any], err: RemorphError): SQL = lift(
    PartialResult(s"!!! ${trees.mkString(" | ")} !!!", err))
  def partialResult(tree: Any, err: RemorphError): SQL = lift(PartialResult(s"!!! $tree !!!", err))

  /**
   * Generate an inline comment that describes the error that was detected in the unresolved relation,
   * which could be parsing errors, or could be something that is not yet implemented. Implemented as
   * a separate method as we may wish to do more with this in the future.
   */
  protected def describeError(relation: ir.Unresolved[_]): SQL = {
    val ruleText =
      if (relation.ruleText.trim.isEmpty) ""
      else
        relation.ruleText
          .split("\n")
          .map {
            case line if line.trim.isEmpty => line.trim
            case line => line.replaceAll(" +$", "")
          }
          .mkString("    ", "\n    ", "")

    val message =
      if (relation.message.trim.isEmpty) ""
      else
        relation.message
          .split("\n")
          .map {
            case line if line.trim.isEmpty => line.trim
            case line => line.replaceAll(" +$", "")
          }
          .mkString("   ", "\n    ", "")

    code"/* The following issues were detected:\n\n$message\n$ruleText\n */"
  }
}
