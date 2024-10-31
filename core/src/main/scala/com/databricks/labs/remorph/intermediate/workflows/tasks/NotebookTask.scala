package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.jdk.CollectionConverters._
import com.databricks.labs.remorph.intermediate.workflows.{JobNode, LeafJobNode}
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Source

case class NotebookTask(
    notebookPath: String,
    baseParameters: Option[Map[String, String]] = None,
    source: Option[Source] = None,
    warehouseId: Option[String] = None)
    extends LeafJobNode
    with CodeAsset {
  override def children: Seq[JobNode] = Seq()
  def toSDK: jobs.NotebookTask = new jobs.NotebookTask()
    .setNotebookPath(notebookPath)
    .setBaseParameters(baseParameters.map(_.asJava).orNull)
    .setSource(source.orNull)
    .setWarehouseId(warehouseId.orNull)
}
