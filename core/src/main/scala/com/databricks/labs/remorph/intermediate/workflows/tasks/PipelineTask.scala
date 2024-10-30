package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class PipelineTask(pipelineId: String, fullRefresh: Boolean) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.PipelineTask = {
    val raw = new jobs.PipelineTask()
    raw
  }
}
