package com.databricks.labs.remorph.intermediate.workflows

import com.databricks.sdk.service.jobs
import com.databricks.sdk.service.jobs.Condition

case class TableUpdateTriggerConfiguration(
    condition: Option[Condition] = None,
    minTimeBetweenTriggersSeconds: Option[Int] = None,
    tableNames: Seq[String] = Seq.empty,
    waitAfterLastChangeSeconds: Option[Int] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ condition
  def toSDK: jobs.TableUpdateTriggerConfiguration = {
    val raw = new jobs.TableUpdateTriggerConfiguration()
    raw
  }
}
