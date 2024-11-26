package com.databricks.labs.remorph.intermediate.adf

case class ParameterDefinition(name: String, value: String) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
