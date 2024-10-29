package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class LocalFileInfo(destination: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.LocalFileInfo = new compute.LocalFileInfo().setDestination(destination)
}
