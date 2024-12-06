package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class AzureKeyVaultSecretReference(
    secretName: String,
    secretVersion: String,
    store: LinkedServiceReference,
    secretType: String)
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq(store)
}
