package com.databricks.labs.remorph.generators.orchestration.rules.bundles

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.fasterxml.jackson.annotation.JsonProperty

case class Bundle(@JsonProperty name: String) extends LeafJobNode
