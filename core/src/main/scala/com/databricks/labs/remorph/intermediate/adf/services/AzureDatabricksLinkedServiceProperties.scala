package com.databricks.labs.remorph.intermediate.adf.services

import com.databricks.labs.remorph.intermediate.adf.PipelineNode

case class AzureDatabricksLinkedServiceProperties(
    annotations: Map[String, String],
    connectVia: Option[IntegrationRuntimeReference],
    description: Option[String],
    parameters: Map[String, String],
    linkedServiceType: Option[String],
    version: Option[String],
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
    extends LinkedServiceProperties(annotations, connectVia, description, parameters, linkedServiceType, version) {
  override def children: Seq[PipelineNode] = super.children ++ accessToken ++
    connectVia ++ credential
}
