package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class SparkPythonTask(pythonFile: String, parameters: Seq[String] = Seq.empty, source: Option[Source] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.SparkPythonTask = {
    val raw = new jobs.SparkPythonTask()
    raw
  }
}
