package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class ActivityPolicy(
    retry: Option[Integer],
    retryIntervalInSeconds: Option[Integer],
    secureInput: Option[Boolean],
    secureOutput: Option[Boolean],
    timeout: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
