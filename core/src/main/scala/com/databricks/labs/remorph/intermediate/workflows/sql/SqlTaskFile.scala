package com.databricks.labs.remorph.intermediate.workflows.sql

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class SqlTaskFile(path: String, source: Option[Source] = None) extends LeafJobNode {
  def toSDK: jobs.SqlTaskFile = new jobs.SqlTaskFile()
    .setPath(path)
    .setSource(source.orNull)
}
