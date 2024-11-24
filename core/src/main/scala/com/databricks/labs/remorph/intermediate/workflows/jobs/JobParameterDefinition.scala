package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class JobParameterDefinition(name: String, default: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobParameterDefinition = new jobs.JobParameterDefinition().setName(name).setDefault(default)
}
