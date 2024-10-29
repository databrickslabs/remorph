package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class JobsHealthRules(rules: Seq[JobsHealthRule] = Seq.empty) extends JobNode {
  override def children: Seq[JobNode] = rules
  def toSDK: jobs.JobsHealthRules = {
    val raw = new jobs.JobsHealthRules()
    raw
  }
}
