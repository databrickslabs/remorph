package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

case class CopyTranslator(
  translatorType: Option[String],
  additionalProperties: Option[TranslatorProperties]
) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
