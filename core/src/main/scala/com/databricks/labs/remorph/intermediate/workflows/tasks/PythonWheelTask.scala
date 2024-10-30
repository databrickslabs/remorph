package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class PythonWheelTask(
    packageName: String,
    entryPoint: String,
    namedParameters: Option[Map[String, String]] = None,
    parameters: Seq[String] = Seq.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.PythonWheelTask = {
    val raw = new jobs.PythonWheelTask()
    raw
  }
}
