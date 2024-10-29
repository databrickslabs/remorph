package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.PauseStatus

case class Continuous(pauseStatus: Option[PauseStatus] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.Continuous = {
    val raw = new jobs.Continuous()
    raw
  }
}
