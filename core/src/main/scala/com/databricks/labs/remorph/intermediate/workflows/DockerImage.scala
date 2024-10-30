package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class DockerImage(basicAuth: Option[DockerBasicAuth], url: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ basicAuth
  def toSDK: compute.DockerImage = {
    val raw = new compute.DockerImage()
    raw
  }
}
