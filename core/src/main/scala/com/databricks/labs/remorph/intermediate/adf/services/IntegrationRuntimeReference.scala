package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class IntegrationRuntimeReference(
    referenceName: String,
    integrationRuntimeType: String,
    parameters: Map[String, String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
