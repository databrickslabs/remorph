package com.databricks.labs.remorph.intermediate.orchestrators.adf.pipelines

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class PipelineFolder(name: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
