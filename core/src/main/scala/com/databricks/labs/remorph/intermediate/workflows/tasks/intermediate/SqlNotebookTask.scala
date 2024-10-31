package com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate

import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.labs.remorph.intermediate.workflows.tasks.{NeedsWarehouse, NotebookTask}
import com.databricks.sdk.service.jobs.Source

case class SqlNotebookTask(plan: LogicalPlan, baseParameters: Map[String, String] = Map.empty)
    extends LeafJobNode
    with ToNotebookTask
    with NeedsWarehouse {
  override def toNotebookTask(notebookPath: String): NotebookTask =
    NotebookTask(notebookPath, Some(baseParameters), Some(Source.WORKSPACE), Some(DEFAULT_WAREHOUSE_ID))
}
