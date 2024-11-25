package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class CredentialReference(referenceName: Option[String], referenceType: Option[CredentialReferenceType])
    extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq() ++ referenceType
}

case class CredentialReferenceType(credentialReference: Option[String]) extends PipelineNode {
  override def children: Seq[PipelineNode] = Seq()
}
