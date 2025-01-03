package com.databricks.labs.remorph.generators.orchestration.rules.bundles

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.fasterxml.jackson.annotation.JsonProperty

case class Schema(
    @JsonProperty("catalog_name") catalogName: String,
    @JsonProperty name: String,
    @JsonProperty comment: Option[String] = None)
    extends LeafJobNode
