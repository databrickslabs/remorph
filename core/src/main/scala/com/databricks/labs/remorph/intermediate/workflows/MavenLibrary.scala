package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute

case class MavenLibrary(coordinates: String, exclusions: Seq[String] = Seq.empty, repo: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.MavenLibrary = {
    val raw = new compute.MavenLibrary()
    raw
  }
}
