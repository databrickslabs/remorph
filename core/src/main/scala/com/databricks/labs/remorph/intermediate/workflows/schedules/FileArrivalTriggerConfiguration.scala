package com.databricks.labs.remorph.intermediate.workflows.schedules

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class FileArrivalTriggerConfiguration(
    url: String,
    minTimeBetweenTriggersSeconds: Option[Int] = None,
    waitAfterLastChangeSeconds: Option[Int] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.FileArrivalTriggerConfiguration = {
    val raw = new jobs.FileArrivalTriggerConfiguration()
    raw
  }
}
