package com.databricks.labs.remorph.intermediate.workflows.schedules

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.PauseStatus

case class CronSchedule(quartzCronExpression: String, timezoneId: String, pauseStatus: Option[PauseStatus] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.CronSchedule = new jobs.CronSchedule()
    .setQuartzCronExpression(quartzCronExpression)
    .setTimezoneId(timezoneId)
    .setPauseStatus(pauseStatus.orNull)
}
