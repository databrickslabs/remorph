package com.databricks.labs.remorph.intermediate.workflows.tasks

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.PipelineParams

case class RunJobTask(
    jobId: Long,
    jobParams: Map[String, String] = Map.empty,
    notebookParams: Map[String, String] = Map.empty,
    pythonNamedParams: Map[String, String] = Map.empty,
    sqlParams: Map[String, String] = Map.empty,
    dbtArgs: Seq[String] = Seq.empty,
    jarParams: Seq[String] = Seq.empty,
    pythonArgs: Seq[String] = Seq.empty,
    sparkSubmitArgs: Seq[String] = Seq.empty,
    fullPipelineRefresh: Boolean = false)
    extends LeafJobNode {
  def toSDK: jobs.RunJobTask = new jobs.RunJobTask()
    .setJobId(jobId)
    .setDbtCommands(dbtArgs.asJava)
    .setJarParams(jarParams.asJava)
    .setJobParameters(jobParams.asJava)
    .setNotebookParams(notebookParams.asJava)
    .setPipelineParams(if (fullPipelineRefresh) new PipelineParams().setFullRefresh(true) else null)
    .setPythonNamedParams(pythonNamedParams.asJava)
    .setPythonParams(pythonArgs.asJava)
    .setSparkSubmitParams(sparkSubmitArgs.asJava)
    .setSqlParams(sqlParams.asJava)
}
