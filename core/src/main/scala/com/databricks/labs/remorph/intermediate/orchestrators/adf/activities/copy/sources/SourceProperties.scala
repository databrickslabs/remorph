package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.sources

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

abstract class SourceProperties(sourceType: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
