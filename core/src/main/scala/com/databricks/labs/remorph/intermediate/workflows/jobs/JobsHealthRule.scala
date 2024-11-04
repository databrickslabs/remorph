package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.{JobsHealthMetric, JobsHealthOperator}

case class JobsHealthRule(metric: JobsHealthMetric, op: JobsHealthOperator, value: Int) extends LeafJobNode {
  def toSDK: jobs.JobsHealthRule = new jobs.JobsHealthRule().setMetric(metric).setOp(op).setValue(value)
}
