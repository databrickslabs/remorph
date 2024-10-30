package com.databricks.labs.remorph.intermediate.workflows.libraries

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class Environment(client: String, dependencies: Seq[String] = Seq.empty) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.Environment = {
    val raw = new compute.Environment()
    raw
  }
}
