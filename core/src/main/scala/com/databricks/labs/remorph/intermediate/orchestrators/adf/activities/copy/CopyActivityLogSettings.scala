package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class CopyActivityLogSettings(
  enableReliableLogging: Option[Boolean],
  logLevel: Option[String]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
