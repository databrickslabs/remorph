package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute
import com.databricks.sdk.service.compute.AzureAvailability

case class AzureAttributes(
    availability: Option[AzureAvailability] = None,
    firstOnDemand: Option[Int] = None,
    logAnalyticsInfo: Option[LogAnalyticsInfo] = None,
    spotBidMaxPrice: Option[Float] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.AzureAttributes = {
    val raw = new compute.AzureAttributes()
    raw
  }
}
