package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class TaskDependency(taskKey: String, outcome: Option[String] = None) extends LeafJobNode {
  def toSDK: jobs.TaskDependency = new jobs.TaskDependency().setTaskKey(taskKey).setOutcome(outcome.orNull)
}
