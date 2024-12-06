package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

sealed trait LibraryDefinition extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
case class FileLibraryDefinition(filePath: String) extends LibraryDefinition
case class MavenLibraryDefinition(coordinates: String, repository: Option[String], exclusions: Option[String])
    extends LibraryDefinition
case class PyPiLibraryDefinition(packageSpecification: String, repository: Option[String]) extends LibraryDefinition
case class CranLibraryDefinition(packageName: String, repository: Option[String]) extends LibraryDefinition
