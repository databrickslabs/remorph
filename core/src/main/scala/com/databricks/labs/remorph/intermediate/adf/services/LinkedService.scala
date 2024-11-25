package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class LinkedService(
    etag: Option[String],
    id: Option[String],
    name: Option[String],
    properties: Option[LinkedServiceProperties],
    linkedServiceType: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ properties
}
