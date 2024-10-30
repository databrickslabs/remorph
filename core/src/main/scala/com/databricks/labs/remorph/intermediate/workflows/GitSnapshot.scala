package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class GitSnapshot(usedCommit: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.GitSnapshot = {
    val raw = new jobs.GitSnapshot()
    raw
  }
}
