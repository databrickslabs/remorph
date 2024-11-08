package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.sdk.service.compute
import com.databricks.sdk.service.compute.{AwsAvailability, EbsVolumeType}

case class AwsAttributes(
    availability: Option[AwsAvailability] = None,
    ebsVolumeCount: Option[Int] = None,
    ebsVolumeIops: Option[Int] = None,
    ebsVolumeSize: Option[Int] = None,
    ebsVolumeThroughput: Option[Int] = None,
    ebsVolumeType: Option[EbsVolumeType] = None,
    firstOnDemand: Option[Int] = None,
    instanceProfileArn: Option[String] = None,
    spotBidPricePercent: Option[Int] = None,
    zoneId: Option[String] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.AwsAttributes = new compute.AwsAttributes()
    .setAvailability(availability.orNull)
    // .setEbsVolumeCount(ebsVolumeCount.orNull)
    // .setEbsVolumeIops(ebsVolumeIops.orNull)
    // .setEbsVolumeSize(ebsVolumeSize.orNull)
    // .setEbsVolumeThroughput(ebsVolumeThroughput.orNull)
    .setEbsVolumeType(ebsVolumeType.orNull)
    // .setFirstOnDemand(firstOnDemand.orNull)
    .setInstanceProfileArn(instanceProfileArn.orNull)
    // .setSpotBidPricePercent(spotBidPricePercent.orNull)
    .setZoneId(zoneId.orNull)
}
