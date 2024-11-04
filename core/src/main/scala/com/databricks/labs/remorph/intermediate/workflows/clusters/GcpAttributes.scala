package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute
import com.databricks.sdk.service.compute.GcpAvailability

case class GcpAttributes(
    availability: Option[GcpAvailability] = None,
    bootDiskSize: Option[Int] = None,
    googleServiceAccount: Option[String] = None,
    localSsdCount: Option[Int] = None,
    usePreemptibleExecutors: Boolean = false,
    zoneId: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.GcpAttributes = {
    val raw = new compute.GcpAttributes()
    raw
  }
}
