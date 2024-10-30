package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class DbtTask(
    commands: Seq[String],
    catalog: Option[String] = None,
    profilesDirectory: Option[String] = None,
    projectDirectory: Option[String] = None,
    schema: Option[String] = None,
    source: Option[Source] = None,
    warehouseId: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.DbtTask = {
    val raw = new jobs.DbtTask()
    raw
  }
}
