package com.databricks.labs.remorph.intermediate.adf.pipelines

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class PipelinePolicy(elapsedTimeMetric: Option[ElapsedTimeMetric]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ elapsedTimeMetric
}
