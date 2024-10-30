package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class DiskSpec(
    diskCount: Option[Int] = None,
    diskIops: Option[Int] = None,
    diskSize: Option[Int] = None,
    diskThroughput: Option[Int] = None,
    diskType: Option[DiskType] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.DiskSpec = {
    val raw = new compute.DiskSpec()
    raw
  }
}
