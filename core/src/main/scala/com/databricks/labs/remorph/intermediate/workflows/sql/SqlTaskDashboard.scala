package com.databricks.labs.remorph.intermediate.workflows.sql

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class SqlTaskDashboard(
    dashboardId: String,
    customSubject: Option[String] = None,
    pauseSubscriptions: Boolean = false,
    subscriptions: Seq[SqlTaskSubscription] = Seq.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ subscriptions
  def toSDK: jobs.SqlTaskDashboard = {
    val raw = new jobs.SqlTaskDashboard()
    raw
  }
}
