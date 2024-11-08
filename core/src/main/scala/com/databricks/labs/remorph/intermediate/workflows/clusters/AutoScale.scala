package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class AutoScale(
    maxWorkers: Option[Int],
    minWorkers: Option[Int] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.AutoScale = new compute.AutoScale()
    // .setMinWorkers(minWorkers.orNull)
    // .setMaxWorkers(maxWorkers.orNull)
}
