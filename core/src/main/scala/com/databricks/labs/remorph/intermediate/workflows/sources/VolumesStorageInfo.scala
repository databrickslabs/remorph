package com.databricks.labs.remorph.intermediate.workflows.sources

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class VolumesStorageInfo(destination: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.VolumesStorageInfo = new compute.VolumesStorageInfo().setDestination(destination)
}
