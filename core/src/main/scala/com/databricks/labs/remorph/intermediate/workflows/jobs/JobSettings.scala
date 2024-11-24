package com.databricks.labs.remorph.intermediate.workflows.jobs

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.schedules.{Continuous, CronSchedule, TriggerSettings}
import com.databricks.labs.remorph.intermediate.workflows.tasks.Task
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.webhooks.WebhookNotifications
import com.databricks.sdk.service.jobs

import java.util.Locale

case class JobSettings(
    name: String,
    tasks: Seq[Task],
    tags: Map[String, String] = Map.empty,
    description: Option[String] = None,
    parameters: Seq[JobParameterDefinition] = Seq.empty,
    jobClusters: Seq[JobCluster] = Seq.empty,
    continuous: Option[Continuous] = None,
    schedule: Option[CronSchedule] = None,
    trigger: Option[TriggerSettings] = None,
    environments: Seq[JobEnvironment] = Seq.empty,
    health: Option[JobsHealthRules] = None,
    timeoutSeconds: Option[Long] = None,
    maxConcurrentRuns: Option[Long] = None,
    runAs: Option[JobRunAs] = None,
    emailNotifications: Option[JobEmailNotifications] = None,
    notificationSettings: Option[JobNotificationSettings] = None,
    webhookNotifications: Option[WebhookNotifications] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ continuous ++ emailNotifications ++
    health ++ notificationSettings ++ runAs ++ schedule ++ trigger ++ webhookNotifications

  def resourceName: String = name.toLowerCase(Locale.ROOT).replaceAll("[^A-Za-z0-9]", "_")

  def toUpdate: jobs.JobSettings = new jobs.JobSettings()
    .setContinuous(continuous.map(_.toSDK).orNull)
    .setDescription(description.orNull)
    .setEmailNotifications(emailNotifications.map(_.toSDK).orNull)
    .setEnvironments(environments.map(_.toSDK).asJava)
    .setHealth(health.map(_.toSDK).orNull)
    .setJobClusters(jobClusters.map(_.toSDK).asJava)
    // .setMaxConcurrentRuns(maxConcurrentRuns.orNull)
    .setName(name)
    .setNotificationSettings(notificationSettings.map(_.toSDK).orNull)
    .setParameters(parameters.map(_.toSDK).asJava)
    .setRunAs(runAs.map(_.toSDK).orNull)
    .setSchedule(schedule.map(_.toSDK).orNull)
    .setTags(tags.asJava)
    .setTasks(tasks.map(_.toSDK).asJava)
    // .setTimeoutSeconds(timeoutSeconds.orNull)
    .setTrigger(trigger.map(_.toSDK).orNull)
    .setWebhookNotifications(webhookNotifications.map(_.toSDK).orNull)

  def toCreate: jobs.CreateJob = new jobs.CreateJob()
    .setContinuous(continuous.map(_.toSDK).orNull)
    .setDescription(description.orNull)
    .setEmailNotifications(emailNotifications.map(_.toSDK).orNull)
    .setEnvironments(environments.map(_.toSDK).asJava)
    .setHealth(health.map(_.toSDK).orNull)
    .setJobClusters(jobClusters.map(_.toSDK).asJava)
    // .setMaxConcurrentRuns(maxConcurrentRuns.orNull)
    .setName(name)
    .setNotificationSettings(notificationSettings.map(_.toSDK).orNull)
    .setParameters(parameters.map(_.toSDK).asJava)
    .setRunAs(runAs.map(_.toSDK).orNull)
    .setSchedule(schedule.map(_.toSDK).orNull)
    .setTags(tags.asJava)
    .setTasks(tasks.map(_.toSDK).asJava)
    // .setTimeoutSeconds(timeoutSeconds.orNull)
    .setTrigger(trigger.map(_.toSDK).orNull)
    .setWebhookNotifications(webhookNotifications.map(_.toSDK).orNull)
}
