package com.databricks.labs.remorph.intermediate.workflows.webhooks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class Webhook(id: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.Webhook = new jobs.Webhook().setId(id)
}
