package com.databricks.labs.remorph.generators.orchestration.rules.history

import com.databricks.labs.remorph.discovery.QueryHistory
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

case class RawMigration(queryHistory: QueryHistory) extends LeafJobNode
