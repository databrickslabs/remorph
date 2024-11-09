package com.databricks.labs.remorph.intermediate.workflows.jobs

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.libraries.Environment
import com.databricks.sdk.service.jobs

case class JobEnvironment(environmentKey: String, spec: Option[Environment] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ spec
  def toSDK: jobs.JobEnvironment = new jobs.JobEnvironment()
    .setEnvironmentKey(environmentKey)
    .setSpec(spec.map(_.toSDK).orNull)
}
