package com.databricks.labs.remorph.intermediate.workflows

case class AutoScale(maxWorkers: Option[Int], minWorkers: Option[Int] = None) extends JobNode {
  override def children: Seq[JobNode] = Seq()

  def toSDK: compute.AutoScale = {
    val raw = new compute.AutoScale()
    raw
  }
}
