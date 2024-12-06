package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class LinkedService(
    etag: String,
    id: String,
    name: String,
    properties: LinkedServiceProperties,
    linkedServiceType: String)
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq(properties)
}
