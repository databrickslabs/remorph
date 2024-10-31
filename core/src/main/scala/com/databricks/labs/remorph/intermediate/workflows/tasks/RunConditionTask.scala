package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.ConditionTaskOp

case class RunConditionTask(op: ConditionTaskOp, left: String, right: String, outcome: Option[String] = None)
    extends LeafJobNode {
  def toSDK: jobs.RunConditionTask = new jobs.RunConditionTask()
    .setOp(op)
    .setLeft(left)
    .setRight(right)
    .setOutcome(outcome.orNull)
}
