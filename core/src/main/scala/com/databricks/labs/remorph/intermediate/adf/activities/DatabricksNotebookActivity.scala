package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class DatabricksNotebookActivity(
    notebookPath: String,
    baseParameters: Map[String, String],
    libraries: Seq[LibraryDefinition])
    extends ActivityProperties {
  override def children: Seq[PipelineNode] = libraries
}
