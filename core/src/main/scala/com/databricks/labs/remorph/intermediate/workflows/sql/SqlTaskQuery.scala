package com.databricks.labs.remorph.intermediate.workflows.sql

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs

case class SqlTaskQuery(queryId: String) extends LeafJobNode {
  def toSDK: jobs.SqlTaskQuery = new jobs.SqlTaskQuery().setQueryId(queryId)
}
