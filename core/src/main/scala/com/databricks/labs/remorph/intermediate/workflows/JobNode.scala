package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.labs.remorph.intermediate.{Origin, TreeNode}

abstract class JobNode(override val origin: Origin = Origin.empty) extends TreeNode[JobNode]()(origin)

abstract class LeafJobNode extends JobNode {
  override def children: Seq[JobNode] = Seq()
}