package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class WorkspaceStorageInfo(destination: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.WorkspaceStorageInfo = new compute.WorkspaceStorageInfo().setDestination(destination)
}
