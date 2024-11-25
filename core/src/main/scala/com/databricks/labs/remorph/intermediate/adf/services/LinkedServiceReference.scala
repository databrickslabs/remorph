package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class LinkedServiceReference(
    parameters: Map[String, String],
    referenceName: Option[String],
    linkedServiceType: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
