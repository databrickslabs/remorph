package com.databricks.labs.remorph.intermediate.workflows.sql

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class SqlTaskSubscription(destinationId: Option[String], userName: Option[String] = None) extends LeafJobNode {
  def toSDK: jobs.SqlTaskSubscription = new jobs.SqlTaskSubscription()
    .setUserName(userName.orNull)
    .setDestinationId(destinationId.orNull)
}
