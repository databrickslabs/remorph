package com.databricks.labs.remorph.intermediate.workflows.schedules

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.PauseStatus

case class Continuous(pauseStatus: Option[PauseStatus] = None) extends LeafJobNode {
  def toSDK: jobs.Continuous = new jobs.Continuous().setPauseStatus(pauseStatus.orNull)
}
