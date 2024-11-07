package com.databricks.labs.remorph.intermediate.orchestrators.adf.activities

import com.databricks.labs.remorph.intermediate.orchestrators.adf.PipelineNode
import com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.{
  CopyTranslator,
  LogSettings,
  RedirectIncompatibleRowSettings,
  SkipErrorFile,
  StagingSettings,
}
import com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.sinks.Sink
import com.databricks.labs.remorph.intermediate.orchestrators.adf.activities.copy.sources.Source
import com.databricks.labs.remorph.intermediate.orchestrators.adf.datasets.DatasetReference

case class CopyActivity(
  activityType: Option[String],
  dataIntegrationUnits: Option[Integer],
  enableSkipIncompatibleRow: Option[Boolean],
  enableStaging: Option[SecureInputOutputPolicy],
  inputs: Seq[DatasetReference],
  logSettings: Option[LogSettings],
  outputs: Seq[DatasetReference],
  parallelCopies: Option[Integer],
  redirectIncompatibleRowSettings: Option[RedirectIncompatibleRowSettings],
  copySink: Option[Sink],
  copySource: Option[Source],
  skipErrorFile: Option[SkipErrorFile],
  stagingSettings: Option[StagingSettings],
  translator: Option[CopyTranslator]
) extends ActivityProperties(activityType) {
  override def children: Seq[PipelineNode] = Seq()
}
