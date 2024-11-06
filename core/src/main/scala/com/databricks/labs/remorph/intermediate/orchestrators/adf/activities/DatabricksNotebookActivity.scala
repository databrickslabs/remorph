package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class DatabricksNotebookActivity(
  activityType: Option[String],
  baseParameters: Map[String, ParameterDefinition],
  libraries: Seq[Map[String, LibraryDefinition]],
  notebookPath: Option[String]
  ) extends AdditionalProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}