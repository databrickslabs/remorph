package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class JobEnvironment(environmentKey: String, spec: Option[Environment] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ spec
  def toSDK: jobs.JobEnvironment = {
    val raw = new jobs.JobEnvironment()
    raw
  }
}
