package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs

case class SqlTaskQuery(queryId: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.SqlTaskQuery = {
    val raw = new jobs.SqlTaskQuery()
    raw
  }
}
