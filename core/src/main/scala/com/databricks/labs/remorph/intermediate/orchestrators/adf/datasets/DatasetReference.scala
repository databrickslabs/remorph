package com.databricks.labs.remorph.intermediate.orchestrators.adf.datasets

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{ParameterDefinition, PipelineNode}

case class DatasetReference(
  parameters: Map[String, ParameterDefinition],
  referenceName: Option[String],
  datasetType: Option[String]
  ) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
