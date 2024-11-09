package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class ForEachTask(inputs: String, task: Task, concurrency: Long = 20) extends JobNode {
  override def children: Seq[JobNode] = Seq(task)
  def toSDK: jobs.ForEachTask = new jobs.ForEachTask()
    .setTask(task.toSDK)
    .setInputs(inputs)
    .setConcurrency(concurrency)
}
