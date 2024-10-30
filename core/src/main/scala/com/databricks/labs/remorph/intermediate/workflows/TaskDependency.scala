package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class TaskDependency(taskKey: String, outcome: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.TaskDependency = {
    val raw = new jobs.TaskDependency()
    raw
  }
}
