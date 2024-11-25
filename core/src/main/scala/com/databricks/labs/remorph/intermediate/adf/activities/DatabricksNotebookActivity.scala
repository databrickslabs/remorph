package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class DatabricksNotebookActivity(
    name: Option[String],
    baseParameters: Map[String, String],
    libraries: Seq[LibraryDefinition],
    notebookPath: Option[String])
    extends ActivityProperties(name) {
  override def children: Seq[PipelineNode] = super.children ++ libraries
}
