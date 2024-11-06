package com.databricks.labs.remorph.intermediate.orchestrators.adf.pipelines

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode
import com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.Activity

case class Pipeline(
                     id: Option[String],
                     name: Option[String],
                     description: Option[String],
                     etag: Option[String],
                     pipelineType: Option[String],
                     activities: Seq[Activity],
                     parameters: Seq[ParameterSpecification],
                     variables: Seq[VariableSpecification],
                     concurrency: Option[Int],
                     folder: Option[PipelineFolder],
                     policy: Option[PipelinePolicy])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
