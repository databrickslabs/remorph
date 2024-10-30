package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class SparkJarTask(jarUri: Option[String], mainClassName: Option[String], parameters: Seq[String] = Seq.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.SparkJarTask = {
    val raw = new jobs.SparkJarTask()
    raw
  }
}
