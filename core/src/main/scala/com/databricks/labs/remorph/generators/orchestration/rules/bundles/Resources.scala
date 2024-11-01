package com.databricks.labs.remorph.generators.orchestration.rules.bundles

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import com.databricks.sdk.service.jobs.CreateJob
import com.fasterxml.jackson.annotation.JsonProperty

case class Resources(
    @JsonProperty jobs: Map[String, CreateJob] = Map.empty,
    @JsonProperty schemas: Map[String, Schema] = Map.empty)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ schemas.values
  def withSchema(schema: Schema): Resources = copy(schemas = schemas + (schema.name -> schema))
  def withJob(job: JobSettings): Resources = {
    val withTarget = job.copy(name = s"[$${bundle.target}] ${job.name}")
    copy(jobs = jobs + (job.resourceName -> withTarget.toCreate))
  }
}
