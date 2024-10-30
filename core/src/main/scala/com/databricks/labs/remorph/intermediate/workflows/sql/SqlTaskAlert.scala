package com.databricks.labs.remorph.intermediate.workflows.sql

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class SqlTaskAlert(
    alertId: String,
    pauseSubscriptions: Boolean = false,
    subscriptions: Seq[SqlTaskSubscription] = Seq.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ subscriptions
  def toSDK: jobs.SqlTaskAlert = {
    val raw = new jobs.SqlTaskAlert()
    raw
  }
}
