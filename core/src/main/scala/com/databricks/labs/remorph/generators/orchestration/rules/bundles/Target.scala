package com.databricks.labs.remorph.generators.orchestration.rules.bundles

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.fasterxml.jackson.annotation.JsonProperty

case class Target(
    @JsonProperty mode: Option[String] = None,
    @JsonProperty default: Boolean = false,
    @JsonProperty resources: Option[Resources] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ resources
}
