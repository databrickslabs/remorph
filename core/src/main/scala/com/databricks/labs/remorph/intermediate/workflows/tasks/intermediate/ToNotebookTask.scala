package com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate

import com.databricks.labs.remorph.intermediate.workflows.tasks.{NotebookTask, Task}

import java.io.File

trait ToNotebookTask extends ToTask {
  def toNotebookTask(notebookPath: String): NotebookTask

  def toTask(path: String): Task = Task(
    taskKey = new File(path).getName,
    description = Some(s"Run notebook $path"),
    notebookTask = Some(toNotebookTask(path)))
}
