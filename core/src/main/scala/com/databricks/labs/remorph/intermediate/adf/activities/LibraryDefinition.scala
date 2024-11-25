package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class LibraryDefinition(
    jarFilePath: Option[String],
    eggFilePath: Option[String],
    whlFilePath: Option[String],
    mavenSpecification: Option[MavenSpecification],
    pyPiSpecification: Option[PyPiSpecification],
    cranSpecification: Option[CranSpecification])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ mavenSpecification ++ pyPiSpecification ++
    cranSpecification
}

case class MavenSpecification(coordinates: String, repository: Option[String], exclusions: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

case class PyPiSpecification(packageSpecification: String, repository: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

case class CranSpecification(packageName: String, repository: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
