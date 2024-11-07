package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.sources

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class Source(
  sourceType: Option[String],
  sourceProperties: Option[SourceProperties],
  disableMetricsCollection: Option[Boolean],
  maxConcurrentConnections: Option[Integer],
  retryCount: Option[Integer],
  retryWait: Option[Integer]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
