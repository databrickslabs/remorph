package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class JobEmailNotifications(
    noAlertForSkippedRuns: Boolean = false,
    onDurationWarningThresholdExceeded: Seq[String] = Seq.empty,
    onFailure: Seq[String] = Seq.empty,
    onStart: Seq[String] = Seq.empty,
    onStreamingBacklogExceeded: Seq[String] = Seq.empty,
    onSuccess: Seq[String] = Seq.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobEmailNotifications = {
    val raw = new jobs.JobEmailNotifications()
    raw
  }
}
