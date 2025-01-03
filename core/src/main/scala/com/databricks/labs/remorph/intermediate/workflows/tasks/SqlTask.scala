package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.jdk.CollectionConverters._
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
    extends JobNode
    with NeedsWarehouse {
  override def children: Seq[JobNode] = Seq() ++ alert ++ dashboard ++ file ++ query
  def toSDK: jobs.SqlTask = new jobs.SqlTask()
    .setWarehouseId(warehouseId)
    .setAlert(alert.map(_.toSDK).orNull)
    .setDashboard(dashboard.map(_.toSDK).orNull)
    .setFile(file.map(_.toSDK).orNull)
    .setParameters(parameters.map(_.asJava).orNull)
    .setQuery(query.map(_.toSDK).orNull)
}
