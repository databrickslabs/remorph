package com.databricks.labs.remorph.intermediate.workflows

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
  def toSDK: jobs.WebhookNotifications = {
    val raw = new jobs.WebhookNotifications()
    raw
  }
}
