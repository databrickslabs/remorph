package com.databricks.labs.remorph.intermediate.orchestrators.adf.services

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{ParameterDefinition, PipelineNode}

case class LinkedServiceReference(
  parameters: Map[String, ParameterDefinition],
  referenceName: Option[String],
  linkedServiceType: Option[String]
  ) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
