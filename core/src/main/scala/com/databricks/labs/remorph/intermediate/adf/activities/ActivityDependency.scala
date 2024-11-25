package com.databricks.labs.remorph.intermediate.adf.activities

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class ActivityDependency(name: Option[String], dependencyConditions: Seq[DependencyCondition])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}

sealed trait DependencyCondition
case object DependencyCompleted extends DependencyCondition
case object DependencyFailed extends DependencyCondition
case object DependencySkipped extends DependencyCondition
case object DependencySucceeded extends DependencyCondition
