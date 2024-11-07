package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode

abstract class TranslatorProperties(translatorType: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
