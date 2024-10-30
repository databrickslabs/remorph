package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.compute
import com.databricks.sdk.service.compute.{DataSecurityMode, RuntimeEngine}

case class NewClusterSpec(
    applyPolicyDefaultValues: Boolean = false,
    autoscale: Option[AutoScale] = None,
    autoterminationMinutes: Option[Int] = None,
    awsAttributes: Option[AwsAttributes] = None,
    azureAttributes: Option[AzureAttributes] = None,
    clusterLogConf: Option[ClusterLogConf] = None,
    clusterName: Option[String] = None,
    customTags: Option[Map[String, String]] = None,
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
    numWorkers: Option[Int] = None,
    policyId: Option[String] = None,
    runtimeEngine: Option[RuntimeEngine] = None,
    singleUserName: Option[String] = None,
    sparkConf: Option[Map[String, String]] = None,
    sparkEnvVars: Option[Map[String, String]] = None,
    sparkVersion: Option[String] = None,
    sshPublicKeys: Seq[String] = Seq.empty,
    workloadType: Option[WorkloadType] = None)
    extends JobNode {
  override def children: Seq[JobNode] = (Seq() ++ autoscale ++ awsAttributes ++ azureAttributes ++
    clusterLogConf ++ gcpAttributes ++ workloadType)
  def toSDK: compute.ClusterSpec = {
    val raw = new compute.ClusterSpec()
    raw
  }
}
