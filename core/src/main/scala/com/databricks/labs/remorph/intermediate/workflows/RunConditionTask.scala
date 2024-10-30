package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.ConditionTaskOp

case class RunConditionTask(op: ConditionTaskOp, left: String, right: String, outcome: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.RunConditionTask = {
    val raw = new jobs.RunConditionTask()
    raw
  }
}
