package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class TypeConversionSettings(
  allowDataTruncation: Option[Boolean],
  culture: Option[String],
  dateTimeFormat: Option[String],
  dateTimeOffsetFormat: Option[String],
  timeSpanFormat: Option[String],
  treatBooleanAsNumber: Option[Boolean]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
