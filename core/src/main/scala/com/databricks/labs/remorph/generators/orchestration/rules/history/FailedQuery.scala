package com.databricks.labs.remorph.generators.orchestration.rules.history

import com.databricks.labs.remorph.WorkflowStage
import com.databricks.labs.remorph.discovery.ExecutedQuery
import com.databricks.labs.remorph.intermediate.workflows.JobNode

case class FailedQuery(query: ExecutedQuery, message: String, stage: WorkflowStage) extends JobNode {
  override def children: Seq[JobNode] = Seq()
}
