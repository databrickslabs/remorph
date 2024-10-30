package com.databricks.labs.remorph.intermediate.workflows.sql

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class SqlTaskFile(path: String, source: Option[Source] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.SqlTaskFile = {
    val raw = new jobs.SqlTaskFile()
    raw
  }
}
