package com.databricks.labs.remorph.intermediate.workflows.libraries

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class Library(
    cran: Option[RCranLibrary] = None,
    egg: Option[String] = None,
    jar: Option[String] = None,
    maven: Option[MavenLibrary] = None,
    pypi: Option[PythonPyPiLibrary] = None,
    requirements: Option[String] = None,
    whl: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ cran ++ maven ++ pypi
  def toSDK: compute.Library = {
    val raw = new compute.Library()
    raw
  }
}
