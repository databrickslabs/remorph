package com.databricks.labs.remorph.intermediate.workflows.libraries

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class PythonPyPiLibrary(spec: String, repo: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.PythonPyPiLibrary = {
    val raw = new compute.PythonPyPiLibrary()
    raw
  }
}
