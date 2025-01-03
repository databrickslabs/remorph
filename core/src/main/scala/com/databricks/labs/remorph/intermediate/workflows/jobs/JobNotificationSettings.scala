package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class JobNotificationSettings(noAlertForCanceledRuns: Boolean = false, noAlertForSkippedRuns: Boolean)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobNotificationSettings = new jobs.JobNotificationSettings()
    .setNoAlertForCanceledRuns(noAlertForCanceledRuns)
    .setNoAlertForSkippedRuns(noAlertForSkippedRuns)
}
