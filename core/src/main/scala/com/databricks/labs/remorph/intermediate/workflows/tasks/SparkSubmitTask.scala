package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class SparkSubmitTask(parameters: Seq[String] = Seq.empty) extends LeafJobNode {
  def toSDK: jobs.SparkSubmitTask = new jobs.SparkSubmitTask().setParameters(parameters.asJava)
}
