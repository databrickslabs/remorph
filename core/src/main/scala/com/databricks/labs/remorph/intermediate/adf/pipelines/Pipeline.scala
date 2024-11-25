package com.databricks.labs.remorph.intermediate.adf.pipelines

import com.databricks.labs.remorph.intermediate.adf.PipelineNode
import com.databricks.labs.remorph.intermediate.adf.activities.Activity

case class Pipeline(
    etag: Option[String],
    id: String,
    name: String,
    activities: Seq[Activity],
    concurrency: Option[Int],
    description: Option[String],
    folder: Option[PipelineFolder],
    parameters: Seq[ParameterSpecification],
    policy: Option[PipelinePolicy],
    variables: Seq[VariableSpecification],
    pipelineType: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ activities ++ parameters ++
    variables ++ folder ++ policy
}
