package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class AzureDatabricksLinkedServiceProperties(
    override val linkedServiceType: String,
    override val annotations: Map[String, String],
    override val connectVia: Option[IntegrationRuntimeReference],
    override val description: Option[String],
    override val parameters: Map[String, String],
    override val version: Option[String],
    accessToken: Option[AzureKeyVaultSecretReference],
    authentication: Option[String],
    credential: Option[CredentialReference],
    domain: Option[String],
    encryptedCredential: Option[String],
    existingClusterId: Option[String],
    instancePoolId: Option[String],
    newClusterCustomTags: Map[String, String],
    newClusterDriverNodeType: Option[String],
    newClusterEnableElasticDisk: Option[Boolean],
    newClusterInitScripts: Seq[String],
    newClusterLogDestination: Seq[String],
    newClusterNodeType: Option[String],
    newClusterNumOfWorker: Option[String],
    newClusterSparkConf: Map[String, String],
    newClusterSparkEnvVars: Map[String, String],
    newClusterVersion: Option[String],
    policyId: Option[String],
    workspaceResourceId: Option[String])
    extends LinkedServiceProperties {
  override def children: Seq[PipelineNode] = Seq() ++ accessToken ++
    connectVia ++ credential
}
