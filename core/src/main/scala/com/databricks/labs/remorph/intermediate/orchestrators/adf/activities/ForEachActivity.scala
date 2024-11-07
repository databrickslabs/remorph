package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{PipelineNode, Expression}

case class ForEachActivity(
  activityType: Option[String],
  activities: Seq[Activity],
  batchCount: Option[Integer],
  isSequential: Option[Boolean],
  items: Option[Expression]
  ) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}
