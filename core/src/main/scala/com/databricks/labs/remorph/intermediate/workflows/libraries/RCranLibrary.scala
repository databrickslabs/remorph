package com.databricks.labs.remorph.intermediate.workflows.libraries

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.compute

case class RCranLibrary(spec: String, repo: Option[String] = None) extends LeafJobNode {
  def toSDK: compute.RCranLibrary = new compute.RCranLibrary().setPackage(spec).setRepo(repo.orNull)
}
