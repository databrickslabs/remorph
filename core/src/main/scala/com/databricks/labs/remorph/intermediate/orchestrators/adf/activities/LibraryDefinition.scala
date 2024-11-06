package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

abstract class LibraryDefinition(libraryType: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

case class JarLibraryDefinition(libraryType: Option[String], path: Option[String])
extends LibraryDefinition(libraryType) {
  override def children: Seq[PipelineNode] = Seq()
}

case class EggLibraryDefinition(libraryType: Option[String], path: Option[String])
  extends LibraryDefinition(libraryType) {
  override def children: Seq[PipelineNode] = Seq()
}

case class WheelLibraryDefinition(libraryType: Option[String], path: Option[String])
  extends LibraryDefinition(libraryType) {
  override def children: Seq[PipelineNode] = Seq()
}

case class PyPiLibraryDefinition(
  libraryType: Option[String],
  packageName: Option[String],
  repo: Option[String]) extends LibraryDefinition(libraryType) {
  override def children: Seq[PipelineNode] = Seq()
}

case class CranLibraryDefinition(
  libraryType: Option[String],
  packageName: Option[String],
  repo: Option[String]) extends LibraryDefinition(libraryType) {
  override def children: Seq[PipelineNode] = Seq()
}

case class MavenLibraryDefinition(
  libraryType: Option[String],
  coordinates: Option[String],
  repo: Option[String],
  exclusions: Option[String]) extends LibraryDefinition(libraryType) {
  override def children: Seq[PipelineNode] = Seq()
}
