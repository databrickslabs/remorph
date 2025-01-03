package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class PipelineTask(pipelineId: String, fullRefresh: Boolean) extends LeafJobNode with CodeAsset {
  def toSDK: jobs.PipelineTask = new jobs.PipelineTask()
    .setPipelineId(pipelineId)
    .setFullRefresh(fullRefresh)
}
