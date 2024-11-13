package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.labs.remorph.intermediate.{Origin, TreeNode}

abstract class JobNode(_origin: Option[Origin] = Option.empty) extends TreeNode[JobNode](_origin)

abstract class LeafJobNode extends JobNode {
  override def children: Seq[JobNode] = Seq()
}