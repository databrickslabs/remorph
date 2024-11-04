package com.databricks.labs.remorph.generators.orchestration.rules.history

import com.databricks.labs.remorph.discovery.ExecutedQuery
import com.databricks.labs.remorph.intermediate.workflows.JobNode

case class PartialQuery(executed: ExecutedQuery, message: String, query: JobNode) extends JobNode {
  override def children: Seq[JobNode] = Seq(query)
}
