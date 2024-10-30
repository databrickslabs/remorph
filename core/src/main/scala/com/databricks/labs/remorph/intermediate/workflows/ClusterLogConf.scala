package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class ClusterLogConf(dbfs: Option[DbfsStorageInfo], s3: Option[S3StorageInfo] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ dbfs ++ s3
  def toSDK: compute.ClusterLogConf = {
    val raw = new compute.ClusterLogConf()
    raw
  }
}
