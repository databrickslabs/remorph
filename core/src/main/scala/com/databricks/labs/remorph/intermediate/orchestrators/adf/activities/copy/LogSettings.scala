package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class LogSettings(
  copyActivityLogSettings: Option[CopyActivityLogSettings],
  enableCopyActivityLog: Option[Boolean],
  logLocationSettings: Option[LogLocationSettings]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
