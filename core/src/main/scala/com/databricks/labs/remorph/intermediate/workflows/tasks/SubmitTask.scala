package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.jobs.{JobEmailNotifications, JobsHealthRules}
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.webhooks.WebhookNotifications
import com.databricks.sdk.service.jobs.{RunIf, RunJobTask}
import com.databricks.sdk.service.{compute, jobs}

case class SubmitTask(
    taskKey: String,
    conditionTask: Option[ConditionTask] = None,
    dbtTask: Option[DbtTask] = None,
    dependsOn: Seq[TaskDependency] = Seq.empty,
    description: Option[String] = None,
    emailNotifications: Option[JobEmailNotifications] = None,
    environmentKey: Option[String] = None,
    existingClusterId: Option[String] = None,
    forEachTask: Option[ForEachTask] = None,
    health: Option[JobsHealthRules] = None,
    libraries: Option[Seq[compute.Library]] = None,
    newCluster: Option[compute.ClusterSpec] = None,
    notebookTask: Option[NotebookTask] = None,
    notificationSettings: Option[TaskNotificationSettings] = None,
    pipelineTask: Option[PipelineTask] = None,
    pythonWheelTask: Option[PythonWheelTask] = None,
    runIf: Option[RunIf] = None,
    runJobTask: Option[RunJobTask] = None,
    sparkJarTask: Option[SparkJarTask] = None,
    sparkPythonTask: Option[SparkPythonTask] = None,
    sparkSubmitTask: Option[SparkSubmitTask] = None,
    sqlTask: Option[SqlTask] = None,
    timeoutSeconds: Option[Int] = None,
    webhookNotifications: Option[WebhookNotifications] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.SubmitTask = {
    val raw = new jobs.SubmitTask()
    raw
  }
}
