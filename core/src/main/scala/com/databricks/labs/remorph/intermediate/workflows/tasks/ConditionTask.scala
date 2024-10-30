package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.ConditionTaskOp

case class ConditionTask(op: ConditionTaskOp, left: String, right: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.ConditionTask = {
    val raw = new jobs.ConditionTask()
    raw
  }
}
