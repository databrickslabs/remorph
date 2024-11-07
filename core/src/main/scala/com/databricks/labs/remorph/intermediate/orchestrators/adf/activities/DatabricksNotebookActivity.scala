package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{ParameterDefinition, PipelineNode}

case class DatabricksNotebookActivity(
  activityType: Option[String],
  baseParameters: Map[String, ParameterDefinition],
  libraries: Seq[Map[String, LibraryDefinition]],
  notebookPath: Option[String]
  ) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}