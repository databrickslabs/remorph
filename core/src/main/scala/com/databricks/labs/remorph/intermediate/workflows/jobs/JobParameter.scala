package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class JobParameter(default: Option[String], name: Option[String], value: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobParameter = {
    val raw = new jobs.JobParameter()
    raw
  }
}
