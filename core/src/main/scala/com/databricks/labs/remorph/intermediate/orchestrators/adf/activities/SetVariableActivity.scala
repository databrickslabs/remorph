package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{Expression, PipelineNode}

case class SetVariableActivity(
  activityType: Option[String],
  variableValue: Option[String],
  variableName: Option[String],
  policy: Option[SecureInputOutputPolicy],
  setSystemVariable: Option[Boolean]
  ) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}
