package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.clusters.ClusterSpec
import com.databricks.sdk.service.jobs

case class JobCluster(jobClusterKey: String, newCluster: ClusterSpec) extends JobNode {
  override def children: Seq[JobNode] = Seq(newCluster)
  def toSDK: jobs.JobCluster = {
    val raw = new jobs.JobCluster()
    raw
  }
}
