package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.{RunIf, RunJobTask}

case class Task(
    taskKey: String,
    conditionTask: Option[ConditionTask] = None,
    dbtTask: Option[DbtTask] = None,
    dependsOn: Seq[TaskDependency] = Seq.empty,
    description: Option[String] = None,
    disableAutoOptimization: Boolean = false,
    emailNotifications: Option[TaskEmailNotifications] = None,
    environmentKey: Option[String] = None,
    existingClusterId: Option[String] = None,
    forEachTask: Option[ForEachTask] = None,
    health: Option[JobsHealthRules] = None,
    jobClusterKey: Option[String] = None,
    libraries: Seq[Library] = Seq.empty,
    maxRetries: Option[Int] = None,
    minRetryIntervalMillis: Option[Int] = None,
    newCluster: Option[NewClusterSpec] = None,
    notebookTask: Option[NotebookTask] = None,
    notificationSettings: Option[TaskNotificationSettings] = None,
    pipelineTask: Option[PipelineTask] = None,
    pythonWheelTask: Option[PythonWheelTask] = None,
    retryOnTimeout: Boolean = false,
    runIf: Option[RunIf] = None,
    runJobTask: Option[RunJobTask] = None,
    sparkJarTask: Option[SparkJarTask] = None,
    sparkPythonTask: Option[SparkPythonTask] = None,
    sparkSubmitTask: Option[SparkSubmitTask] = None,
    sqlTask: Option[SqlTask] = None,
    timeoutSeconds: Option[Int] = None,
    webhookNotifications: Option[WebhookNotifications] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() // TODO: Add all the children

  def toSDK: jobs.Task = {
    val raw = new jobs.Task()
    raw
  }
}
