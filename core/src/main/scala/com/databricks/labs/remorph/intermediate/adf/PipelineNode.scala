package com.databricks.labs.remorph.intermediate.adf

import com.databricks.labs.remorph.intermediate.TreeNode

abstract class PipelineNode extends TreeNode[PipelineNode]

abstract class LeafPipelineNode extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}