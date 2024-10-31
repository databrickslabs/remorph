package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

case class InformationFile(id: String, text: String) extends LeafJobNode
