package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class NotebookTask(
    notebookPath: String,
    baseParameters: Option[Map[String, String]] = None,
    source: Option[Source] = None,
    warehouseId: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.NotebookTask = {
    val raw = new jobs.NotebookTask()
    raw
  }
}
