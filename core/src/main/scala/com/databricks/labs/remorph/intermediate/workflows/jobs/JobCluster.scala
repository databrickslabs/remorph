package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.clusters.NewClusterSpec
import com.databricks.sdk.service.jobs

case class JobCluster(jobClusterKey: String, newCluster: NewClusterSpec) extends JobNode {
  override def children: Seq[JobNode] = Seq(newCluster)
  def toSDK: jobs.JobCluster = new jobs.JobCluster()
    .setJobClusterKey(jobClusterKey)
    .setNewCluster(newCluster.toSDK)
}
