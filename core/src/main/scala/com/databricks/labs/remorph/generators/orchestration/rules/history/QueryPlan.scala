package com.databricks.labs.remorph.generators.orchestration.rules.history

import com.databricks.labs.remorph.discovery.ExecutedQuery
import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

case class QueryPlan(plan: LogicalPlan, query: ExecutedQuery) extends LeafJobNode
