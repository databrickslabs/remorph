package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

case class SuccessPy(id: String, code: String) extends LeafJobNode
