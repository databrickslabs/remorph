package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.labs.remorph.intermediate.TreeNode

abstract class JobNode extends TreeNode[JobNode]

abstract class LeafJobNode extends JobNode {
  override def children: Seq[JobNode] = Seq()
}