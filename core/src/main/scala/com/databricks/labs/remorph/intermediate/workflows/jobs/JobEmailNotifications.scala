package com.databricks.labs.remorph.intermediate.workflows.jobs

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class JobEmailNotifications(
    noAlertForSkippedRuns: Boolean = false,
    onDurationWarningThresholdExceeded: Seq[String] = Seq.empty,
    onFailure: Seq[String] = Seq.empty,
    onStart: Seq[String] = Seq.empty,
    onStreamingBacklogExceeded: Seq[String] = Seq.empty,
    onSuccess: Seq[String] = Seq.empty)
    extends LeafJobNode {
  def toSDK: jobs.JobEmailNotifications = new jobs.JobEmailNotifications()
    .setNoAlertForSkippedRuns(noAlertForSkippedRuns)
    .setOnDurationWarningThresholdExceeded(onDurationWarningThresholdExceeded.asJava)
    .setOnFailure(onFailure.asJava)
    .setOnStart(onStart.asJava)
    .setOnStreamingBacklogExceeded(onStreamingBacklogExceeded.asJava)
    .setOnSuccess(onSuccess.asJava)
}
