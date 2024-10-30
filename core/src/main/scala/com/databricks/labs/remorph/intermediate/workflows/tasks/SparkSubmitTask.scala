package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class SparkSubmitTask(parameters: Seq[String] = Seq.empty) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.SparkSubmitTask = {
    val raw = new jobs.SparkSubmitTask()
    raw
  }
}
