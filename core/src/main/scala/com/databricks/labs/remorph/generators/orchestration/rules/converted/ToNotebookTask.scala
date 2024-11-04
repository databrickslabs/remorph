package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.tasks.{NotebookTask, Task}

trait ToNotebookTask extends ToTask {
  def resourceName: String
  def toNotebookTask: NotebookTask
  def toTask: Task = Task(taskKey = resourceName, notebookTask = Some(toNotebookTask))
}
