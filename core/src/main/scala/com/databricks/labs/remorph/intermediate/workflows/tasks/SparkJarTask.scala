package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class SparkJarTask(jarUri: Option[String], mainClassName: Option[String], parameters: Seq[String] = Seq.empty)
    extends LeafJobNode {
  def toSDK: jobs.SparkJarTask = new jobs.SparkJarTask()
    .setJarUri(jarUri.orNull)
    .setMainClassName(mainClassName.orNull)
    .setParameters(parameters.asJava)
}
