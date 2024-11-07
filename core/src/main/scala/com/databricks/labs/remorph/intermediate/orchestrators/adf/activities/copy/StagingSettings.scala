package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode
import com.databricks.labs.remorph.intermediate.orchestrators.adf.services.LinkedServiceReference

case class StagingSettings(
  additionalProperties: Map[String, String],
  enableCompression: Option[Boolean],
  linkedServiceReference: Option[LinkedServiceReference],
  path: Option[String]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
