package com.databricks.labs.remorph.intermediate.workflows.libraries

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.compute

case class PythonPyPiLibrary(spec: String, repo: Option[String] = None) extends LeafJobNode {
  def toSDK: compute.PythonPyPiLibrary = new compute.PythonPyPiLibrary().setPackage(spec).setRepo(repo.orNull)
}
