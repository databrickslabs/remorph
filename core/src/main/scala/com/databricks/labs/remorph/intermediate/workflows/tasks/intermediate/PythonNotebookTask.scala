package com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.labs.remorph.intermediate.workflows.tasks.NotebookTask
import com.databricks.sdk.service.jobs.Source

case class PythonNotebookTask(code: String, baseParameters: Map[String, String] = Map.empty)
    extends LeafJobNode
    with ToNotebookTask {
  override def toNotebookTask(notebookPath: String): NotebookTask =
    NotebookTask(notebookPath, Some(baseParameters), Some(Source.WORKSPACE), None)
}
