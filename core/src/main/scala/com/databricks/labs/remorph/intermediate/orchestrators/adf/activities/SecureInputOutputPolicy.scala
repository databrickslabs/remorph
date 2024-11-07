package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{Expression, PipelineNode}

case class SecureInputOutputPolicy(
  secureInput: Option[Boolean],
  secureOutput: Option[Boolean]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
