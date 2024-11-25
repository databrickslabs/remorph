package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

abstract class ActivityProperties(name: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
