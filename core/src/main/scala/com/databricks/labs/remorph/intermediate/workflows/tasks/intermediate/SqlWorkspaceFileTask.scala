package com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate

import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.labs.remorph.intermediate.workflows.sql.SqlTaskFile
import com.databricks.labs.remorph.intermediate.workflows.tasks.{NeedsWarehouse, SqlTask, Task}
import com.databricks.sdk.service.jobs.Source

import java.io.File

case class SqlWorkspaceFileTask(plan: LogicalPlan, parameters: Map[String, String] = Map.empty)
    extends LeafJobNode
    with ToTask
    with NeedsWarehouse {
  override def toTask(path: String): Task = Task(
    taskKey = new File(path).getName,
    description = Some(s"Run notebook $path"),
    sqlTask = Some(
      SqlTask(
        warehouseId = DEFAULT_WAREHOUSE_ID,
        parameters = Some(parameters),
        file = Some(SqlTaskFile(path, Some(Source.WORKSPACE))))))
}
