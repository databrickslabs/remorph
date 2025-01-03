package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class TaskNotificationSettings(
    alertOnLastAttempt: Boolean = false,
    noAlertForCanceledRuns: Boolean = false,
    noAlertForSkippedRuns: Boolean)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.TaskNotificationSettings = {
    val raw = new jobs.TaskNotificationSettings()
    raw
  }
}
