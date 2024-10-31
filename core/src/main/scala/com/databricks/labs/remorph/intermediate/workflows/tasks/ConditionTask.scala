package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.ConditionTaskOp

case class ConditionTask(op: ConditionTaskOp, left: String, right: String) extends LeafJobNode {
  def toSDK: jobs.ConditionTask = new jobs.ConditionTask()
    .setOp(op)
    .setLeft(left)
    .setRight(right)
}
