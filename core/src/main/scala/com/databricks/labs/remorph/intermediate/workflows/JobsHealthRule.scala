package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.{JobsHealthMetric, JobsHealthOperator}

case class JobsHealthRule(metric: JobsHealthMetric, op: JobsHealthOperator, value: Int) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobsHealthRule = {
    val raw = new jobs.JobsHealthRule()
    raw
  }
}
