package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.sinks

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

abstract class SinkProperties(sinkType: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
