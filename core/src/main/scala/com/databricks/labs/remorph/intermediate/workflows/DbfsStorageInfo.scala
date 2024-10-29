package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class DbfsStorageInfo(destination: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.DbfsStorageInfo = new compute.DbfsStorageInfo().setDestination(destination)
}
