package com.databricks.labs.remorph.intermediate.workflows.jobs

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs

case class JobsHealthRules(rules: Seq[JobsHealthRule]) extends JobNode {
  override def children: Seq[JobNode] = rules
  def toSDK: jobs.JobsHealthRules = new jobs.JobsHealthRules().setRules(rules.map(_.toSDK).asJava)
}
