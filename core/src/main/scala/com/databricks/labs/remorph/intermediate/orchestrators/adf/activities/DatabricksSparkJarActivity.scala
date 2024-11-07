package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{ParameterDefinition, PipelineNode}

case class DatabricksSparkJarActivity(
  activityType: Option[String],
  mainClassName: Option[String],
  parameters: Seq[ParameterDefinition],
  libraries: Seq[Map[String, LibraryDefinition]]
  ) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}
