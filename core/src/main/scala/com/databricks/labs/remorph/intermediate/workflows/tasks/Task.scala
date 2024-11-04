package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.clusters.NewClusterSpec
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobsHealthRules
import com.databricks.labs.remorph.intermediate.workflows.libraries.Library
import com.databricks.labs.remorph.intermediate.workflows._
import com.databricks.labs.remorph.intermediate.workflows.webhooks.WebhookNotifications
import com.databricks.sdk.service.jobs

case class Task(
    taskKey: String,
    description: Option[String] = None,
    dependsOn: Seq[TaskDependency] = Seq.empty,
    dbtTask: Option[DbtTask] = None,
    conditionTask: Option[ConditionTask] = None,
    forEachTask: Option[ForEachTask] = None,
    notebookTask: Option[NotebookTask] = None,
    pipelineTask: Option[PipelineTask] = None,
    pythonWheelTask: Option[PythonWheelTask] = None,
    runJobTask: Option[RunJobTask] = None,
    sparkJarTask: Option[SparkJarTask] = None,
    sparkPythonTask: Option[SparkPythonTask] = None,
    sparkSubmitTask: Option[SparkSubmitTask] = None,
    sqlTask: Option[SqlTask] = None,
    libraries: Seq[Library] = Seq.empty,
    newCluster: Option[NewClusterSpec] = None,
    existingClusterId: Option[String] = None,
    jobClusterKey: Option[String] = None,
    runIf: Option[jobs.RunIf] = None,
    disableAutoOptimization: Boolean = false,
    environmentKey: Option[String] = None,
    maxRetries: Option[Int] = None,
    minRetryIntervalMillis: Option[Int] = None,
    health: Option[JobsHealthRules] = None,
    retryOnTimeout: Boolean = false,
    timeoutSeconds: Option[Int] = None,
    notificationSettings: Option[TaskNotificationSettings] = None,
    emailNotifications: Option[TaskEmailNotifications] = None,
    webhookNotifications: Option[WebhookNotifications] = None)
    extends JobNode {

  override def children: Seq[JobNode] = Seq() ++
    conditionTask ++
    dbtTask ++
    dependsOn ++
    emailNotifications ++
    forEachTask ++
    health ++
    libraries ++
    newCluster ++
    notebookTask ++
    notificationSettings ++
    pipelineTask ++
    pythonWheelTask ++
    runJobTask ++
    sparkJarTask ++
    sparkPythonTask ++
    sparkSubmitTask ++
    sqlTask ++
    webhookNotifications

  def dependOn(task: Task): Task = copy(dependsOn = dependsOn :+ TaskDependency(task.taskKey))

  def toSDK: jobs.Task = new jobs.Task()
    .setTaskKey(taskKey)
    .setConditionTask(conditionTask.map(_.toSDK).orNull)
    .setDbtTask(dbtTask.map(_.toSDK).orNull)
    .setDependsOn(dependsOn.map(_.toSDK).asJava)
    .setDescription(description.orNull)
    .setDisableAutoOptimization(disableAutoOptimization)
    .setEmailNotifications(emailNotifications.map(_.toSDK).orNull)
    .setEnvironmentKey(environmentKey.orNull)
    .setExistingClusterId(existingClusterId.orNull)
    .setForEachTask(forEachTask.map(_.toSDK).orNull)
    .setHealth(health.map(_.toSDK).orNull)
    .setJobClusterKey(jobClusterKey.orNull)
    .setLibraries(libraries.map(_.toSDK).asJava)
    .setMaxRetries(maxRetries.map(_.asInstanceOf[java.lang.Long]).orNull)
    .setMinRetryIntervalMillis(minRetryIntervalMillis.map(_.asInstanceOf[java.lang.Long]).orNull)
    .setNewCluster(newCluster.map(_.toSDK).orNull)
    .setNotebookTask(notebookTask.map(_.toSDK).orNull)
    .setNotificationSettings(notificationSettings.map(_.toSDK).orNull)
    .setPipelineTask(pipelineTask.map(_.toSDK).orNull)
    .setPythonWheelTask(pythonWheelTask.map(_.toSDK).orNull)
    .setRetryOnTimeout(retryOnTimeout)
    .setRunIf(runIf.orNull)
    .setRunJobTask(runJobTask.map(_.toSDK).orNull)
    .setSparkJarTask(sparkJarTask.map(_.toSDK).orNull)
    .setSparkPythonTask(sparkPythonTask.map(_.toSDK).orNull)
    .setSparkSubmitTask(sparkSubmitTask.map(_.toSDK).orNull)
    .setSqlTask(sqlTask.map(_.toSDK).orNull)
    .setTimeoutSeconds(timeoutSeconds.map(_.asInstanceOf[java.lang.Long]).orNull)
    .setWebhookNotifications(webhookNotifications.map(_.toSDK).orNull)
}
