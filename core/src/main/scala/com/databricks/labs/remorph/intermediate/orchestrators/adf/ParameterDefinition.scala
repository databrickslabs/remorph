package com.databricks.labs.remorph.intermediate.orchestrators.adf

case class ParameterDefinition(name: Option[String], value: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
