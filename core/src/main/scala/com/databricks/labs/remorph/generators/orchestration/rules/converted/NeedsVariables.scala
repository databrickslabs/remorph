package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.JobNode

case class NeedsVariables(child: JobNode, variables: Seq[String]) extends JobNode {
  override def children: Seq[JobNode] = Seq(child)
}
