package com.databricks.labs.remorph.intermediate.orchestrators.adf.pipelines

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode
import java.time.Duration

case class ElapsedTimeMetric(duration: Option[Duration]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
