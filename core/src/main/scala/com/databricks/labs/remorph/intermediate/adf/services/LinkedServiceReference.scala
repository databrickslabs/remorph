package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class LinkedServiceReference(referenceName: String, linkedServiceType: String, parameters: Map[String, String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
