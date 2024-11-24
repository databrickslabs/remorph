package com.databricks.labs.remorph.intermediate.workflows.libraries

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.compute

case class MavenLibrary(coordinates: String, exclusions: Seq[String] = Seq.empty, repo: Option[String] = None)
    extends LeafJobNode {
  def toSDK: compute.MavenLibrary = new compute.MavenLibrary()
    .setCoordinates(coordinates)
    .setExclusions(exclusions.asJava)
    .setRepo(repo.orNull)
}
