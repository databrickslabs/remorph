package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.sql.SqlTaskFile
import com.databricks.labs.remorph.intermediate.workflows.tasks.{NeedsWarehouse, SqlTask, Task}

case class SqlWorkspaceFileTask(file: CreatedFile, parameters: Map[String, String] = Map.empty)
    extends JobNode
    with ToTask
    with NeedsWarehouse {
  override def children: Seq[JobNode] = Seq(file)
  override def toTask: Task = Task(
    taskKey = file.resourceName,
    sqlTask = Some(
      SqlTask(warehouseId = DEFAULT_WAREHOUSE_ID, parameters = Some(parameters), file = Some(SqlTaskFile(file.name)))))
}
