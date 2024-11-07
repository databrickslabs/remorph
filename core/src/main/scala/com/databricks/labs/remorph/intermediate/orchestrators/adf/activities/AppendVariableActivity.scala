package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class AppendVariableActivity(
  activityType: Option[String],
  variableValue: Option[String],
  variableName: Option[String],
  ) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}
