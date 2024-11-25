package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

abstract class LinkedServiceProperties(
    annotations: Map[String, String],
    connectVia: Option[IntegrationRuntimeReference],
    description: Option[String],
    parameters: Map[String, String],
    linkedServiceType: Option[String],
    version: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ connectVia
}
