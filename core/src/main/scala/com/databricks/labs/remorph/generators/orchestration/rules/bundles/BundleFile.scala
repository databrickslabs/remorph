package com.databricks.labs.remorph.generators.orchestration.rules.bundles

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.fasterxml.jackson.annotation.JsonProperty

case class BundleFile(
    @JsonProperty bundle: Option[Bundle] = None,
    @JsonProperty targets: Map[String, Target] = Map.empty,
    @JsonProperty resources: Option[Resources] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ bundle ++ resources ++ targets.values
}
