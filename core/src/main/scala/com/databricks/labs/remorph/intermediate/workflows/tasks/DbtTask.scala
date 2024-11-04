package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.jdk.CollectionConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
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
    extends LeafJobNode
    with NeedsWarehouse {
  def toSDK: jobs.DbtTask = new jobs.DbtTask()
    .setCommands(commands.asJava)
    .setCatalog(catalog.orNull)
    .setProfilesDirectory(profilesDirectory.orNull)
    .setProjectDirectory(projectDirectory.orNull)
    .setSchema(schema.orNull)
    .setSource(source.orNull)
    .setWarehouseId(warehouseId.orNull)
}
