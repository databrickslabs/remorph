package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class AzureKeyVaultSecretReference(
    secretName: Option[String],
    secretVersion: Option[String],
    store: Option[LinkedServiceReference],
    secretType: Option[String])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ store
}
