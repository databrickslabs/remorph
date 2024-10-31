package com.databricks.labs.remorph.intermediate.workflows.libraries

import scala.collection.JavaConverters._
import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode
import com.databricks.sdk.service.compute

case class Environment(client: String, dependencies: Seq[String] = Seq.empty) extends LeafJobNode {
  def toSDK: compute.Environment = new compute.Environment().setClient(client).setDependencies(dependencies.asJava)
}
