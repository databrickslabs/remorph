package com.databricks.labs.remorph.intermediate.orchestrators.adf

case class Expression(expressionType: Option[String], expressionValue: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
