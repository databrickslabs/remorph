package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.JobSourceDirtyState

case class JobSource(jobConfigPath: String, importFromGitBranch: String, dirtyState: Option[JobSourceDirtyState] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobSource = {
    val raw = new jobs.JobSource()
    raw
  }
}
