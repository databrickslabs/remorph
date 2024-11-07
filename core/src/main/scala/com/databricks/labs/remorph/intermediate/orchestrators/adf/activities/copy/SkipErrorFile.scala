package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class SkipErrorFile(
  dataInconsistency: Option[Boolean],
  fileMissing: Option[Boolean]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
