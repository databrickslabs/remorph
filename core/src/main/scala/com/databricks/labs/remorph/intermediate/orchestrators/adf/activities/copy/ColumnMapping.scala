package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class ColumnMapping(
  source: MappingElement,
  sink: MappingElement
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

case class MappingElement(
  fieldName: Option[String],
  dataType: Option[String]
)
