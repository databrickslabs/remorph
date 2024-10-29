package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.labs.remorph.intermediate.TreeNode
import com.databricks.sdk.service.compute._
import com.databricks.sdk.service.jobs._
import com.databricks.sdk.service.{compute, jobs}

abstract class JobNode extends TreeNode[JobNode]

case class Adlsgen2Info(destination: String) extends JobNode {
  override def children: Seq[JobNode] = Seq()
  def toSDK: compute.Adlsgen2Info = new compute.Adlsgen2Info().setDestination(destination)
}













































































































































