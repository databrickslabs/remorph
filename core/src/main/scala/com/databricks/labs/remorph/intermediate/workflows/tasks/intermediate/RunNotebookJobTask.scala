package com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import com.databricks.labs.remorph.intermediate.workflows.tasks.RunJobTask

case class RunNotebookJobTask(job: JobSettings, params: Map[String, String] = Map.empty) extends JobNode {
  override def children: Seq[JobNode] = Seq(job)
  def toRunJobTask(id: Long): RunJobTask = RunJobTask(id, notebookParams = params)
}
