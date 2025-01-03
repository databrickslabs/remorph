package com.databricks.labs.remorph.intermediate.workflows.clusters

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.libraries.DockerImage
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute
import com.databricks.sdk.service.compute.{DataSecurityMode, RuntimeEngine}

case class NewClusterSpec(
    applyPolicyDefaultValues: Boolean = false,
    autoscale: Option[AutoScale] = None,
    autoterminationMinutes: Option[Long] = None,
    awsAttributes: Option[AwsAttributes] = None,
    azureAttributes: Option[AzureAttributes] = None,
    clusterLogConf: Option[ClusterLogConf] = None,
    clusterName: Option[String] = None,
    customTags: Map[String, String] = Map.empty,
    dataSecurityMode: Option[DataSecurityMode] = None,
    dockerImage: Option[DockerImage] = None,
    driverInstancePoolId: Option[String] = None,
    driverNodeTypeId: Option[String] = None,
    enableElasticDisk: Boolean = false,
    enableLocalDiskEncryption: Boolean = false,
    gcpAttributes: Option[GcpAttributes] = None,
    initScripts: Seq[InitScriptInfo] = Seq.empty,
    instancePoolId: Option[String] = None,
    nodeTypeId: Option[String] = None,
    numWorkers: Option[Long] = None,
    policyId: Option[String] = None,
    runtimeEngine: Option[RuntimeEngine] = None,
    singleUserName: Option[String] = None,
    sparkConf: Map[String, String] = Map.empty,
    sparkEnvVars: Map[String, String] = Map.empty,
    sparkVersion: Option[String] = None,
    sshPublicKeys: Seq[String] = Seq.empty,
    workloadType: Option[WorkloadType] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ autoscale ++ awsAttributes ++ azureAttributes ++
    clusterLogConf ++ gcpAttributes ++ workloadType ++ dockerImage ++ initScripts
  def toSDK: compute.ClusterSpec = new compute.ClusterSpec()
    .setApplyPolicyDefaultValues(applyPolicyDefaultValues)
    .setAutoscale(autoscale.map(_.toSDK).orNull)
    // .setAutoterminationMinutes(autoterminationMinutes.getOrElse(null))
    .setAwsAttributes(awsAttributes.map(_.toSDK).orNull)
    .setAzureAttributes(azureAttributes.map(_.toSDK).orNull)
    .setGcpAttributes(gcpAttributes.map(_.toSDK).orNull)
    .setClusterLogConf(clusterLogConf.map(_.toSDK).orNull)
    .setClusterName(clusterName.orNull)
    .setCustomTags(customTags.asJava)
    .setDataSecurityMode(dataSecurityMode.orNull)
    .setDockerImage(dockerImage.map(_.toSDK).orNull)
    .setInstancePoolId(instancePoolId.orNull)
    .setDriverInstancePoolId(driverInstancePoolId.orNull)
    .setDriverNodeTypeId(driverNodeTypeId.orNull)
    .setEnableElasticDisk(enableElasticDisk)
    .setEnableLocalDiskEncryption(enableLocalDiskEncryption)
    .setInitScripts(initScripts.map(_.toSDK).asJava)
    .setNodeTypeId(nodeTypeId.orNull)
    // .setNumWorkers(numWorkers.orNull)
    .setPolicyId(policyId.orNull)
    .setRuntimeEngine(runtimeEngine.orNull)
    .setSingleUserName(singleUserName.orNull)
    .setSparkConf(sparkConf.asJava)
    .setSparkEnvVars(sparkEnvVars.asJava)
    .setSparkVersion(sparkVersion.orNull)
    .setSshPublicKeys(sshPublicKeys.asJava)
    .setWorkloadType(workloadType.map(_.toSDK).orNull)
}
