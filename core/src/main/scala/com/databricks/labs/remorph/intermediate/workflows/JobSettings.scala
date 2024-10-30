package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.{Format, JobEditMode}

case class JobSettings(
    budgetPolicyId: Option[String] = None,
    continuous: Option[Continuous] = None,
    deployment: Option[JobDeployment] = None,
    description: Option[String] = None,
    editMode: Option[JobEditMode] = None,
    emailNotifications: Option[JobEmailNotifications] = None,
    environments: Seq[JobEnvironment] = Seq.empty,
    format: Option[Format] = None,
    gitSource: Option[GitSource] = None,
    health: Option[JobsHealthRules] = None,
    jobClusters: Seq[JobCluster] = Seq.empty,
    maxConcurrentRuns: Option[Int] = None,
    name: Option[String] = None,
    notificationSettings: Option[JobNotificationSettings] = None,
    parameters: Seq[JobParameterDefinition] = Seq.empty,
    runAs: Option[JobRunAs] = None,
    schedule: Option[CronSchedule] = None,
    tags: Option[Map[String, String]] = None,
    tasks: Seq[Task] = Seq.empty,
    timeoutSeconds: Option[Int] = None,
    trigger: Option[TriggerSettings] = None,
    webhookNotifications: Option[WebhookNotifications] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ continuous ++ deployment ++ emailNotifications ++
    gitSource ++ health ++ notificationSettings ++ runAs ++ schedule ++ trigger ++ webhookNotifications
  def toSDK: jobs.JobSettings = {
    val raw = new jobs.JobSettings()
    raw
  }
}
