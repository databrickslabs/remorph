package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class CredentialReference(referenceName: String, referenceType: CredentialReferenceType) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq(referenceType)
}

case class CredentialReferenceType(credentialReference: String) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
