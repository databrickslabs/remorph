package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class WorkloadType(clients: ClientsTypes) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.WorkloadType = {
    val raw = new compute.WorkloadType()
    raw
  }
}