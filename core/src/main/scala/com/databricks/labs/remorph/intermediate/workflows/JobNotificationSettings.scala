package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class JobNotificationSettings(noAlertForCanceledRuns: Boolean = false, noAlertForSkippedRuns: Boolean)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobNotificationSettings = {
    val raw = new jobs.JobNotificationSettings()
    raw
  }
}
