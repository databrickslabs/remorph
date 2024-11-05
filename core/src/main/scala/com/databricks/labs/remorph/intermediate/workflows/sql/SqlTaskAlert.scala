package com.databricks.labs.remorph.intermediate.workflows.sql

import scala.jdk.CollectionConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class SqlTaskAlert(
    alertId: String,
    pauseSubscriptions: Boolean = false,
    subscriptions: Seq[SqlTaskSubscription] = Seq.empty)
    extends LeafJobNode {
  def toSDK: jobs.SqlTaskAlert = new jobs.SqlTaskAlert()
    .setAlertId(alertId)
    .setPauseSubscriptions(pauseSubscriptions)
    .setSubscriptions(subscriptions.map(_.toSDK).asJava)
}
