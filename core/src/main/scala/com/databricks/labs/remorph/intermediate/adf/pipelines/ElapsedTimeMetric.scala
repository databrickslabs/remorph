package com.databricks.labs.remorph.intermediate.adf.pipelines

import com.databricks.labs.remorph.intermediate.adf.PipelineNode
import java.time.Duration

case class ElapsedTimeMetric(duration: Option[Duration]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
