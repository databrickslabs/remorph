package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.sources.{DbfsStorageInfo, S3StorageInfo}
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class ClusterLogConf(dbfs: Option[DbfsStorageInfo], s3: Option[S3StorageInfo] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ dbfs ++ s3
  def toSDK: compute.ClusterLogConf = new compute.ClusterLogConf()
    .setDbfs(dbfs.map(_.toSDK).orNull)
    .setS3(s3.map(_.toSDK).orNull)
}
