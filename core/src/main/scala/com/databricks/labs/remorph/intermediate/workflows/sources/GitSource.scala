package com.databricks.labs.remorph.intermediate.workflows.sources

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSource
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.GitProvider

case class GitSource(
    gitUrl: String,
    gitProvider: GitProvider,
    gitBranch: Option[String] = None,
    gitCommit: Option[String] = None,
    gitSnapshot: Option[GitSnapshot] = None,
    gitTag: Option[String] = None,
    jobSource: Option[JobSource] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.GitSource = {
    val raw = new jobs.GitSource()
    raw
  }
}
