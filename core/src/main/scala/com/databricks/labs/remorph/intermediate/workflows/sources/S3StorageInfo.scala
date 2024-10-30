package com.databricks.labs.remorph.intermediate.workflows.sources

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class S3StorageInfo(
    destination: String,
    cannedAcl: Option[String] = None,
    enableEncryption: Boolean = false,
    encryptionType: Option[String] = None,
    endpoint: Option[String] = None,
    kmsKey: Option[String] = None,
    region: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.S3StorageInfo = {
    val raw = new compute.S3StorageInfo()
    raw
  }
}
