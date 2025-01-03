package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class SparkPythonTask(pythonFile: String, parameters: Seq[String] = Seq.empty, source: Option[Source] = None)
    extends LeafJobNode
    with CodeAsset {
  def toSDK: jobs.SparkPythonTask = new jobs.SparkPythonTask()
    .setPythonFile(pythonFile)
    .setParameters(parameters.asJava)
    .setSource(source.orNull)
}
