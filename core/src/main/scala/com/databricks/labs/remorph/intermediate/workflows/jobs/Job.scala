package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class Job(
    createdTime: Option[Int] = None,
    creatorUserName: Option[String] = None,
    effectiveBudgetPolicyId: Option[String] = None,
    jobId: Option[Int] = None,
    runAsUserName: Option[String] = None,
    settings: Option[JobSettings] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ settings
  def toSDK: jobs.Job = {
    val raw = new jobs.Job()
    raw
  }
}
