package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class ClientsTypes(jobs: Boolean = false, notebooks: Boolean) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.ClientsTypes = {
    val raw = new compute.ClientsTypes()
    raw
  }
}
