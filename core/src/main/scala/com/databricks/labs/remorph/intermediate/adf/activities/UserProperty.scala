package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class UserProperty(name: String, value: String) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
