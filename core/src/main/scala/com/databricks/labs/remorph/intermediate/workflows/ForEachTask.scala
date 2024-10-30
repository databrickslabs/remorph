package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class ForEachTask(inputs: String, task: Task, concurrency: Option[Int] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq(task)
  def toSDK: jobs.ForEachTask = {
    val raw = new jobs.ForEachTask()
    raw
  }
}
