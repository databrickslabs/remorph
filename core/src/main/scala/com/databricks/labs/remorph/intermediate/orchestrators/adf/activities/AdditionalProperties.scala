package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

abstract class AdditionalProperties(activityType: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
