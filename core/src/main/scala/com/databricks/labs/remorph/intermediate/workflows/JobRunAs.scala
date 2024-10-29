package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class JobRunAs(servicePrincipalName: Option[String], userName: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobRunAs = {
    val raw = new jobs.JobRunAs()
    raw
  }
}
