package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import com.databricks.labs.remorph.intermediate.workflows.tasks.RunJobTask

// TODO: if we have this node, then add new rule to inject DynamicJobs(m: Migration, deploying: Map[Int,String])
// and replace the in-memory integers with `"${resources.jobs.STRING.id}"` in low-level YAML rewrite
case class RunNotebookJobTask(job: JobSettings, params: Map[String, String] = Map.empty) extends JobNode {
  override def children: Seq[JobNode] = Seq(job)
  def toRunJobTask(id: Long): RunJobTask = RunJobTask(id, notebookParams = params)
}
