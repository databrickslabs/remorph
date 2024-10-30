package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class JobParameterDefinition(name: String, default: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobParameterDefinition = {
    val raw = new jobs.JobParameterDefinition()
    raw
  }
}
