package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

trait LinkedServiceProperties extends PipelineNode {
  def linkedServiceType: String
  def annotations: Map[String, String]
  def connectVia: Option[IntegrationRuntimeReference]
  def description: Option[String]
  def parameters: Map[String, String]
  def version: Option[String]
}
