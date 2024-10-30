package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class DockerBasicAuth(password: Option[String], username: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.DockerBasicAuth = {
    val raw = new compute.DockerBasicAuth()
    raw
  }
}