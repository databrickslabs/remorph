package com.databricks.labs.remorph.intermediate.workflows.webhooks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class WebhookNotifications(
    onDurationWarningThresholdExceeded: Seq[Webhook] = Seq.empty,
    onFailure: Seq[Webhook] = Seq.empty,
    onStart: Seq[Webhook] = Seq.empty,
    onStreamingBacklogExceeded: Seq[Webhook] = Seq.empty,
    onSuccess: Seq[Webhook] = Seq.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ onDurationWarningThresholdExceeded ++ onFailure ++
    onStart ++ onStreamingBacklogExceeded ++ onSuccess
  def toSDK: jobs.WebhookNotifications = new jobs.WebhookNotifications()
    .setOnDurationWarningThresholdExceeded(onDurationWarningThresholdExceeded.map(_.toSDK).asJava)
    .setOnFailure(onFailure.map(_.toSDK).asJava)
    .setOnStart(onStart.map(_.toSDK).asJava)
    .setOnStreamingBacklogExceeded(onStreamingBacklogExceeded.map(_.toSDK).asJava)
    .setOnSuccess(onSuccess.map(_.toSDK).asJava)
}
