package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows._
import com.databricks.labs.remorph.intermediate.workflows.sql.{SqlTaskAlert, SqlTaskDashboard, SqlTaskFile, SqlTaskQuery}
import com.databricks.sdk.service.jobs

case class SqlTask(
    warehouseId: String,
    alert: Option[SqlTaskAlert] = None,
    dashboard: Option[SqlTaskDashboard] = None,
    file: Option[SqlTaskFile] = None,
    parameters: Option[Map[String, String]] = None,
    query: Option[SqlTaskQuery] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ alert ++ dashboard ++ file ++ query
  def toSDK: jobs.SqlTask = {
    val raw = new jobs.SqlTask()
    raw
  }
}
