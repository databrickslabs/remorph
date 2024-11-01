package com.databricks.labs.remorph.generators.orchestration.rules.bundles

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

case class JobReference(name: String) extends LeafJobNode
