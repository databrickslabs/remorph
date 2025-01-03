package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.tasks.Task

trait ToTask {
  def toTask: Task
}
