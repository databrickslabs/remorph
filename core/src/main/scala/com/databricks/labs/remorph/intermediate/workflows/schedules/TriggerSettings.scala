package com.databricks.labs.remorph.intermediate.workflows.schedules

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.PauseStatus

case class TriggerSettings(
    fileArrival: Option[FileArrivalTriggerConfiguration] = None,
    pauseStatus: Option[PauseStatus] = None,
    periodic: Option[PeriodicTriggerConfiguration] = None,
    table: Option[TableUpdateTriggerConfiguration] = None,
    tableUpdate: Option[TableUpdateTriggerConfiguration] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ fileArrival ++ periodic ++ table ++ tableUpdate
  def toSDK: jobs.TriggerSettings = {
    val raw = new jobs.TriggerSettings()
    raw
  }
}
