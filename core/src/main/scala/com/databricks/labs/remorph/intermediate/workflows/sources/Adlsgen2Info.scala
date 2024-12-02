package com.databricks.labs.remorph.intermediate.workflows.sources

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute

case class Adlsgen2Info(destination: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.Adlsgen2Info = new compute.Adlsgen2Info().setDestination(destination)
}
