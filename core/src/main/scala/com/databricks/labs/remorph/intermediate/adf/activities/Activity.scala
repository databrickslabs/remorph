package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode
import com.databricks.labs.remorph.intermediate.adf.services.LinkedServiceReference

case class Activity(
    dependsOn: Seq[ActivityDependency],
    description: Option[String],
    linkedServiceName: Option[LinkedServiceReference],
    name: Option[String],
    onInactiveMarkAs: Option[OnInactiveMarkAs],
    policy: Option[ActivityPolicy],
    state: Option[ActivityState],
    activityType: Option[String],
    activityProperties: Option[ActivityProperties],
    userProperties: Seq[UserProperty])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ dependsOn ++ linkedServiceName ++
    policy ++ userProperties
}

sealed trait ActivityState
case object Active extends ActivityState
case object Inactive extends ActivityState

sealed trait OnInactiveMarkAs
case object MarkAsFailed extends OnInactiveMarkAs
case object MarkAsSkipped extends OnInactiveMarkAs
case object MarkAsSucceeded extends OnInactiveMarkAs
