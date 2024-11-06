package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class ActivityDependency(
    name: Option[String],
    additionalProperties: Seq[AdditionalProperties],
    dependencyConditions: Seq[DependencyCondition])
  extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

sealed trait DependencyCondition
case object Completed extends DependencyCondition
case object Failed extends DependencyCondition
case object Skipped extends DependencyCondition
case object Succeeded extends DependencyCondition
