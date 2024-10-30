package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute
import com.databricks.sdk.service.compute.{DiskTypeAzureDiskVolumeType, DiskTypeEbsVolumeType}

case class DiskType(
    azureDiskVolumeType: Option[DiskTypeAzureDiskVolumeType] = None,
    ebsVolumeType: Option[DiskTypeEbsVolumeType] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.DiskType = {
    val raw = new compute.DiskType()
    raw
  }
}
