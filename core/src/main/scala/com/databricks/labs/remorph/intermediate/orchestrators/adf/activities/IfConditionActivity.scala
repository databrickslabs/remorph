package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{Expression, PipelineNode}

case class IfConditionActivity(
  activityType: Option[String],
  expression: Option[Expression],
  ifFalseActivities: Seq[Activity],
  ifTrueActivities: Seq[Activity]
  ) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}
