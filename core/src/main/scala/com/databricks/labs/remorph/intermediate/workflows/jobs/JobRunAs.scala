package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class JobRunAs(servicePrincipalName: Option[String], userName: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobRunAs = new jobs.JobRunAs()
    .setServicePrincipalName(servicePrincipalName.orNull)
    .setUserName(userName.orNull)
}
