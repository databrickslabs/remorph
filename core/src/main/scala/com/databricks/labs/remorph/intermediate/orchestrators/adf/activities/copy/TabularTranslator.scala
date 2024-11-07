package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy

import com.databricks.labs.remorph.intermediate.orchestrators.adf.{Expression, PipelineNode}

case class TabularTranslator(
  translatorType: Option[String],
  collectionReference: Option[String],
  mapComplexValuesToString: Option[Boolean],
  mappings: Seq[ColumnMapping],
  typeConversion: Option[Boolean],
  typeConversionSettings: Option[TypeConversionSettings]
) extends TranslatorProperties(translatorType) {
  override def children: Seq[PipelineNode] = Seq()
}
