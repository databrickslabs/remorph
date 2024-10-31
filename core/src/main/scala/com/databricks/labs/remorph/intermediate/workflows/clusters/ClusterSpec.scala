package com.databricks.labs.remorph.intermediate.workflows.clusters

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.libraries.Library
import com.databricks.sdk.service.jobs

case class ClusterSpec(
    existingClusterId: Option[String] = None,
    jobClusterKey: Option[String] = None,
    libraries: Seq[Library] = Seq.empty,
    newCluster: Option[NewClusterSpec] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ libraries ++ newCluster
  def toSDK: jobs.ClusterSpec = new jobs.ClusterSpec()
    .setExistingClusterId(existingClusterId.orNull)
    .setJobClusterKey(jobClusterKey.orNull)
    .setLibraries(libraries.map(_.toSDK).asJava)
    .setNewCluster(newCluster.map(_.toSDK).orNull)
}
