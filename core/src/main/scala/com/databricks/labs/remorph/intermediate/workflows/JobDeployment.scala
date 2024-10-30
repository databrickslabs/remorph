package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.JobDeploymentKind

case class JobDeployment(kind: JobDeploymentKind, metadataFilePath: Option[String] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.JobDeployment = {
    val raw = new jobs.JobDeployment()
    raw
  }
}
