package com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate

import com.databricks.labs.remorph.intermediate.workflows.tasks.Task

trait ToTask {
  def toTask(path: String): Task
}
