package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

case class SuccessSQL(id: String, query: String) extends LeafJobNode
