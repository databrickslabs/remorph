package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class Activity(
    name: Option[String],
    description: Option[String],
    activityType: Option[String],
    dependsOn: Seq[ActivityDependency],
    state: Option[ActivityState],
    onInactiveMarkAs: Option[OnInactiveMarkAs],
    additionalProperties: Seq[AdditionalProperties],
    userProperties: Seq[UserProperty])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

sealed trait ActivityState
case object Active extends ActivityState
case object Inactive extends ActivityState

sealed trait OnInactiveMarkAs
case object Failed extends OnInactiveMarkAs
case object Skipped extends OnInactiveMarkAs
case object Succeeded extends OnInactiveMarkAs
