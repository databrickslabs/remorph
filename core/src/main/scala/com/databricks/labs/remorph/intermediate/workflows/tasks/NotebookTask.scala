package com.databricks.labs.remorph.intermediate.workflows.tasks

import com.databricks.labs.remorph.intermediate.workflows.{JobNode, LeafJobNode}
import com.databricks.sdk.service.jobs

import scala.jdk.CollectionConverters._

case class NotebookTask(
    notebookPath: String,
    baseParameters: Option[Map[String, String]] = None,
    warehouseId: Option[String] = None)
    extends LeafJobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.NotebookTask = new jobs.NotebookTask()
    .setNotebookPath(notebookPath)
    .setBaseParameters(baseParameters.map(_.asJava).orNull)
    .setWarehouseId(warehouseId.orNull)
}
