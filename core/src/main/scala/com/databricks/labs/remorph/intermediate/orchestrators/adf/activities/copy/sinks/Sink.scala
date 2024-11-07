package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.sinks

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class Sink(
  sinkType: Option[String],
  sinkProperties: Option[SinkProperties],
  disableMetricsCollection: Option[Boolean],
  maxConcurrentConnections: Option[Integer],
  retryCount: Option[Integer],
  retryWait: Option[Integer]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
