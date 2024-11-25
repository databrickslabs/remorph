package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class IntegrationRuntimeReference(
    parameters: Map[String, String],
    referenceName: Option[String],
    integrationRuntimeType: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
