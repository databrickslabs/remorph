package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode
import com.databricks.labs.remorph.intermediate.adf.services.LinkedServiceReference

case class Activity(
    name: String,
    activityType: String,
    activityProperties: ActivityProperties,
    state: ActivityState,
    dependsOn: Seq[ActivityDependency],
    description: Option[String],
    linkedServiceName: Option[LinkedServiceReference],
    onInactiveMarkAs: Option[OnInactiveMarkAs],
    policy: Option[ActivityPolicy],
    userProperties: Seq[UserProperty])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = dependsOn ++ linkedServiceName ++ onInactiveMarkAs ++
    policy ++ userProperties ++ Seq(activityProperties, state)
}

sealed trait ActivityState extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
case object ActiveState extends ActivityState
case object InactiveState extends ActivityState
case object UnknownState extends ActivityState

sealed trait OnInactiveMarkAs extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
case object MarkAsFailed extends OnInactiveMarkAs
case object MarkAsSkipped extends OnInactiveMarkAs
case object MarkAsSucceeded extends OnInactiveMarkAs
