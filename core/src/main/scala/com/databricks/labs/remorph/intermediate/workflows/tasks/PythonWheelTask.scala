package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class PythonWheelTask(
    packageName: String,
    entryPoint: String,
    namedParameters: Option[Map[String, String]] = None,
    parameters: Seq[String] = Seq.empty)
    extends LeafJobNode
    with CodeAsset {
  def toSDK: jobs.PythonWheelTask = new jobs.PythonWheelTask()
    .setPackageName(packageName)
    .setEntryPoint(entryPoint)
    .setNamedParameters(namedParameters.getOrElse(Map.empty).asJava)
    .setParameters(parameters.asJava)
}
